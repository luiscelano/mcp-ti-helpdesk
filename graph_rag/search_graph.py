import os
from pathlib import Path
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from neo4j import GraphDatabase

GRAPH_SOURCE_ID = "archivo2_grafo.csv"


def _get_neo4j_connection_settings() -> Tuple[str, str, str, str]:
    root_dir = Path(__file__).resolve().parent.parent
    load_dotenv(root_dir / ".env")

    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")

    missing = [
        name
        for name, value in [
            ("NEO4J_URI", uri),
            ("NEO4J_USERNAME", username),
            ("NEO4J_PASSWORD", password),
        ]
        if not value
    ]
    if missing:
        raise ValueError(f"Missing environment variables: {missing}")

    return str(uri), str(username), str(password), str(database)


def search_graph(node_name: str, depth: int = 2) -> Dict[str, object]:
    uri, username, password, database = _get_neo4j_connection_settings()
    driver = GraphDatabase.driver(uri, auth=(username, password))

    direct_relations_query = """
    MATCH (origin:Entity {name: $node_name})-[relation:RELATION {source: $source_id}]->(destination:Entity)
    RETURN origin.name AS origin, relation.type AS relation, destination.name AS destination
    ORDER BY destination.name ASC
    """

    two_hop_query = """
    MATCH path=(origin:Entity {name: $node_name})-[first:RELATION {source: $source_id}]->(middle:Entity)
    OPTIONAL MATCH (middle)-[second:RELATION {source: $source_id}]->(destination:Entity)
    RETURN origin.name AS origin, middle.name AS middle, destination.name AS destination
    ORDER BY middle.name ASC, destination.name ASC
    """

    direct_relations: List[Dict[str, str]] = []
    second_level: List[Dict[str, str]] = []

    try:
        with driver.session(database=database) as session:
            for row in session.run(
                direct_relations_query,
                node_name=node_name,
                source_id=GRAPH_SOURCE_ID,
            ):
                direct_relations.append(
                    {
                        "origin": row["origin"],
                        "relation": row["relation"],
                        "destination": row["destination"],
                    }
                )

            if depth >= 2:
                for row in session.run(
                    two_hop_query,
                    node_name=node_name,
                    source_id=GRAPH_SOURCE_ID,
                ):
                    if row["destination"] is None:
                        continue
                    if row["destination"] == row["middle"]:
                        continue
                    second_level.append(
                        {
                            "origin": row["origin"],
                            "middle": row["middle"],
                            "destination": row["destination"],
                        }
                    )
    finally:
        driver.close()

    return {
        "query": node_name,
        "direct_relations": direct_relations,
        "two_hop_paths": second_level,
    }


def format_graph_response(result: Dict[str, object]) -> List[str]:
    lines: List[str] = []

    for relation in result.get("direct_relations", []):
        lines.append(f"{relation['origin']} -> {relation['destination']}")

    seen = set(lines)
    for path in result.get("two_hop_paths", []):
        line = f"{path['middle']} -> {path['destination']}"
        if line not in seen:
            lines.append(line)
            seen.add(line)

    return lines
