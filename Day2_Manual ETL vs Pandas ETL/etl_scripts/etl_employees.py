import pandas as pd
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)
DATA_DIR = Path(__file__).parent.parent / "data"


def main():
    input_path = DATA_DIR / "input" / "employess.csv"
    output_path = DATA_DIR / "output" / "employees_summary.csv"

    logger.info("Reading input CSV...")
    df = pd.read_csv(input_path)
    logger.info(f"Initial row count: {len(df)}")

    # 1.Add full_name column
    df["full_name"] = df["first_name"] + " " + df["last_name"]

    # 2. Increase salary by 10% for Engineering department
    """
    .loc means “location-based indexer” — it lets you pick rows and columns by labels.
    syntax : df.loc[<row_condition>, <column_selection>]

So here:

df.loc[df["department"] == "Engineering", "salary"]
means:

“Select the salary column for all rows where department == Engineering.”
    """

    df.loc[df["department"] == "Engineering", "salary"] *= 1.10

    # 3. Drop rows with any nulls
    df.dropna(inplace=True)
    logger.info(f"Row count after cleaning: {len(df)}")

    # 4. Add a timestamp column
    df["updated_at"] = pd.Timestamp.now()

    # 5.Write Output to JSON
    """
    df.to_json(output_path, orient="records", indent=4)
Writes the DataFrame to JSON with one object per row. orient="records" produces a list of objects like your earlier manual list[dict].
    """
    # df.to_json(output_path, orient="records", indent=4)
    df.to_json(output_path, orient="records", indent=4)
    logger.info(f"Wrote cleaned data to {output_path}")

    # 6. Verify
    check = pd.read_json(output_path)
    logger.info(f"Verified Row count in output: {len(check)} records.")


if __name__ == "__main__":
    main()
