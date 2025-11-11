from etl_scripts.file_handler import read_csv, write_csv, read_json
from utils.logger import get_logger
from pathlib import Path

logger = get_logger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"


def main():
    users_csv = DATA_DIR / "input" / "users.csv"
    sales_json = DATA_DIR / "input" / "sales.json"
    output_csv = DATA_DIR / "output" / "transformed_data.csv"

    users = read_csv(users_csv)
    sales = read_json(sales_json)

    transformed = [
        {"username": u["name"], "email": u["email"], "sales_count": len(sales)}
        for u in users
    ]

    if transformed:
        write_csv(output_csv, transformed, ["username", "email", "sales_count"])
        logger.info("Transformation Comapleted!")
    else:
        logger.warning("No data transformed!")


if __name__ == "__main__":
    main()
