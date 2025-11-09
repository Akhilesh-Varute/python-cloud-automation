import sys, csv, logging, os
from collections import Counter

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),  # write to file
        logging.StreamHandler(),  # show in console
    ],
)


def count_lines(file_path):
    logging.info(f"Counting lines from file {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        # lines = [line.strip() for line in lines]
    return Counter(lines)


def save_lines_count_to_csv(counts, output_path):
    logging.info(f"saving lines count to {output_path}")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["line", "count"])
        for line, cnt in counts.items():
            writer.writerow([line.strip(), cnt])


def main():
    if len(sys.argv) != 3:
        logging.error("Usage: python line_count.py input.txt output.csv")
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]
    logging.info("Starting line count process")
    counts = count_lines(input_path)
    save_lines_count_to_csv(counts, output_path)
    logging.info(f"Processed {len(counts)} unique lines -> saved in {output_path}")


if __name__ == "__main__":
    main()
