import json
import os
from typing import Dict

from dotenv import load_dotenv
from neo4j import GraphDatabase


def run_connectivity_check() -> Dict[str, object]:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(root_dir, ".env"))

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
        return {
            "status": "fail",
            "authenticated": False,
            "query_ok": False,
            "database": database,
            "error": f"Missing environment variables: {', '.join(missing)}",
        }

    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session(database=database) as session:
            record = session.run("RETURN 1 AS ok").single()
            query_ok = bool(record and record.get("ok") == 1)

        return {
            "status": "pass" if query_ok else "fail",
            "authenticated": True,
            "query_ok": query_ok,
            "database": database,
            "error": None if query_ok else "Validation query returned unexpected result",
        }
    except Exception as exc:  # pragma: no cover
        return {
            "status": "fail",
            "authenticated": False,
            "query_ok": False,
            "database": database,
            "error": str(exc),
        }
    finally:
        if driver is not None:
            driver.close()


def main() -> int:
    result = run_connectivity_check()
    print(json.dumps(result, ensure_ascii=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
