import sys
import pandas as pd

from sqlalchemy import text
from tabulate import tabulate

from db import get_engine

def main():

    sql = open("sql/04_data_quality.sql").read()

    with get_engine().connect() as conn:

        df = pd.read_sql(
            text(sql),
            conn
        )

    df["status"] = (
        df["expected"] == df["actual"]
    ).map({
        True: "PASS",
        False: "FAIL"
    })

    print(
        tabulate(
            df,
            headers="keys",
            tablefmt="github",
            showindex=False
        )
    )

    if (df["status"] == "FAIL").any():

        print("\nDATA QUALITY GATE FAILED")
        sys.exit(1)

    print("\nAll data quality checks passed")

if __name__ == "__main__":
    main()
