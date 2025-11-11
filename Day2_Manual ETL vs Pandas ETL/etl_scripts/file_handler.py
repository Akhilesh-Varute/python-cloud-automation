import csv, json, os
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"


def read_csv(file_path):
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = list(reader)
            logger.info(f"Read {len(data)} records from {file_path}")
            return data
    except Exception as e:
        logger.error((f"Failed to read CSV file {file_path}: {e}"))
        return []


def write_csv(file_path, data, fieldnames):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            logger.info(f"Wrote {len(data)} records to {file_path}")
    except Exception as e:
        logger.error(f"Failed to write in csv file {file_path}: {e}")


def read_json(file_path):
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Read JSON data from {file_path}")
            return data
    except Exception as e:
        logger.error(f"Failed to read JSON file {file_path}: {e}")
        return []


def write_json(file_path, data):
    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Wrote JSON data to {file_path}")
    except Exception as e:
        logger.error(f"Failed to write JSON file {file_path}: {e}")
