#!/usr/bin/env python3
import sys
import csv
import time
import logging
from logging.handlers import RotatingFileHandler
from collections import Counter
import argparse

# -------- Logging setup --------
LOG_FILE = "logs/line_count.log"


def setup_logging(log_file=LOG_FILE):
    # Create logs dir if needed
    import os

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger("line_counter")
    logger.setLevel(logging.DEBUG)  # capture everything, filter in handlers

    # Console handler (INFO+)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    ch.setFormatter(ch_formatter)

    # Rotating file handler (DEBUG+)
    fh = RotatingFileHandler(
        log_file, maxBytes=5_000_000, backupCount=5, encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    fh.setFormatter(fh_formatter)

    # Avoid duplicate handlers if setup_logging is called twice
    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger


logger = setup_logging()


# -------- Core logic --------
def count_lines(file_path, skip_empty=True, normalize=True):
    """
    Count unique lines in a file.
    - skip_empty: ignore blank lines
    - normalize: strip whitespace from ends
    """
    with open(file_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    if normalize:
        lines = [ln.strip() for ln in raw_lines]
    else:
        lines = [ln.rstrip("\n") for ln in raw_lines]

    if skip_empty:
        lines = [ln for ln in lines if ln]

    return Counter(lines)


def save_lines_count_to_csv(counts, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["line", "count"])
        for line, cnt in counts.items():
            writer.writerow([line, cnt])


# -------- CLI + main --------
def parse_args():
    p = argparse.ArgumentParser(
        description="Count unique lines in a text file and save counts to CSV."
    )
    p.add_argument("input", help="Path to input text file")
    p.add_argument("output", help="Path to output CSV file")
    p.add_argument("--skip-empty", action="store_true", help="Skip blank lines")
    p.add_argument(
        "--no-normalize",
        dest="normalize",
        action="store_false",
        help="Don't strip whitespace from lines",
    )
    return p.parse_args()


def main():
    args = parse_args()
    start = time.time()
    logger.info("Starting line_count run: input=%s output=%s", args.input, args.output)

    try:
        counts = count_lines(
            args.input, skip_empty=args.skip_empty, normalize=args.normalize
        )
        save_lines_count_to_csv(counts, args.output)
        duration = time.time() - start
        logger.info(
            "Completed: %d unique lines -> %s (%.2fs)",
            len(counts),
            args.output,
            duration,
        )
        # Example debug info: top 5 most common lines
        top5 = counts.most_common(5)
        logger.debug("Top 5 lines: %s", top5)
    except FileNotFoundError as e:
        logger.error("Input file not found: %s", args.input)
        logger.debug("Exception details:", exc_info=True)
        sys.exit(2)
    except Exception:
        # Logs full stack trace
        logger.exception("Unhandled error during processing")
        sys.exit(3)


if __name__ == "__main__":
    main()
