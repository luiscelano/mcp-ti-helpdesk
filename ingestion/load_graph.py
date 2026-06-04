import csv
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from neo4j import GraphDatabase

GRAPH_SOURCE_ID = "archivo2_grafo.csv"


def read_graph_csv(source_path: str | Path = "data/archivo2_grafo.csv") -> List[Tuple[str, str, str]]:
    path = Path(source_path)
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        expected_headers = ["entidad_origen", "relacion", "entidad_destino"]
        if reader.fieldnames != expected_headers:
            raise ValueError(
                "CSV headers must be entidad_origen,relacion,entidad_destino"
            )

        rows: List[Tuple[str, str, str]] = []
        for row in reader:
            rows.append(
                (
                    str(row["entidad_origen"]).strip(),
                    str(row["relacion"]).strip(),
                    str(row["entidad_destino"]).strip(),
                )
            )

        if not rows:
            raise ValueError("Graph CSV must contain at least one relation")

        return rows


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


def load_graph_from_csv(source_path: str | Path = "data/archivo2_grafo.csv") -> Dict[str, object]:
    rows = read_graph_csv(source_path)
    uri, username, password, database = _get_neo4j_connection_settings()

    query = """
    MERGE (o:Entity {name: $origin})
    MERGE (d:Entity {name: $destination})
    MERGE (o)-[r:RELATION {type: $relation, source: $source_id}]->(d)
    RETURN elementId(r) AS relationship_id
    """

    loaded_relationships = 0
    driver = GraphDatabase.driver(uri, auth=(username, password))
    try:
        with driver.session(database=database) as session:
            for origin, relation, destination in rows:
                session.run(
                    query,
                    origin=origin,
                    relation=relation,
                    destination=destination,
                    source_id=GRAPH_SOURCE_ID,
                ).single()
                loaded_relationships += 1
    finally:
        driver.close()

    return {
        "source": str(source_path),
        "relationships_loaded": loaded_relationships,
        "database": database,
    }


def run_graph_validation_queries() -> Dict[str, bool]:
    uri, username, password, database = _get_neo4j_connection_settings()
    driver = GraphDatabase.driver(uri, auth=(username, password))

    expected_graph_001 = {
        ("AccesoBloqueado", "DesbloqueoIAM"),
        ("DesbloqueoIAM", "VerificacionIdentidad"),
        ("DesbloqueoIAM", "OficialCumplimiento"),
    }
    expected_graph_002 = {
        ("IncidenteImpresion", "ReiniciarCola"),
        ("IncidenteImpresion", "ReinstalarControladores"),
    }
    expected_graph_003 = {
        ("SistemaPrestamos", "ProblemaSSL"),
        ("ProblemaSSL", "VerificarCertificados"),
    }

    try:
        with driver.session(database=database) as session:
            graph_001_result = session.run(
                """
                MATCH (o:Entity)-[r:RELATION {source: $source_id}]->(d:Entity)
                WHERE (o.name = 'AccesoBloqueado' AND d.name = 'DesbloqueoIAM')
                   OR (o.name = 'DesbloqueoIAM' AND d.name = 'VerificacionIdentidad')
                   OR (o.name = 'DesbloqueoIAM' AND d.name = 'OficialCumplimiento')
                RETURN o.name AS origin, d.name AS destination
                """,
                source_id=GRAPH_SOURCE_ID,
            )
            graph_001_pairs = {(r["origin"], r["destination"]) for r in graph_001_result}

            graph_002_result = session.run(
                """
                MATCH (o:Entity {name: 'IncidenteImpresion'})-[r:RELATION {source: $source_id}]->(d:Entity)
                RETURN o.name AS origin, d.name AS destination
                """,
                source_id=GRAPH_SOURCE_ID,
            )
            graph_002_pairs = {(r["origin"], r["destination"]) for r in graph_002_result}

            graph_003_result = session.run(
                """
                MATCH (o:Entity)-[r:RELATION {source: $source_id}]->(d:Entity)
                WHERE (o.name = 'SistemaPrestamos' AND d.name = 'ProblemaSSL')
                   OR (o.name = 'ProblemaSSL' AND d.name = 'VerificarCertificados')
                RETURN o.name AS origin, d.name AS destination
                """,
                source_id=GRAPH_SOURCE_ID,
            )
            graph_003_pairs = {(r["origin"], r["destination"]) for r in graph_003_result}

            return {
                "GRAPH-001": expected_graph_001.issubset(graph_001_pairs),
                "GRAPH-002": expected_graph_002.issubset(graph_002_pairs),
                "GRAPH-003": expected_graph_003.issubset(graph_003_pairs),
            }
    finally:
        driver.close()


def main() -> int:
    load_result = load_graph_from_csv()
    validation_result = run_graph_validation_queries()
    payload = {
        "load": load_result,
        "validation": validation_result,
    }
    print(json.dumps(payload, ensure_ascii=True))

    return 0 if all(validation_result.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
