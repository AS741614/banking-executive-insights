import logging
import pandas as pd

from pathlib import Path
from sqlalchemy import text

from db import get_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

log = logging.getLogger("etl")

RAW = Path("data/raw")

TABLES = [
    "branches",
    "products",
    "customers",
    "accounts",
    "transactions"
]

def run_sql_file(conn, path):
    sql = Path(path).read_text()
    conn.execute(text(sql))

def main():

    engine = get_engine()

    with engine.begin() as conn:

        log.info("Applying warehouse schema")
        run_sql_file(conn, "sql/01_schema.sql")

        for table in TABLES:

            df = pd.read_csv(RAW / f"{table}.csv")

            conn.execute(
                text(f"TRUNCATE staging.{table}")
            )

            df.to_sql(
                table,
                conn,
                schema="staging",
                if_exists="append",
                index=False
            )

            log.info(
                "Loaded %s → staging (%d rows)",
                table,
                len(df)
            )

        log.info("Running transformations")
        run_sql_file(conn, "sql/02_transform.sql")

        log.info("ETL pipeline completed successfully")

if __name__ == "__main__":
    main()
