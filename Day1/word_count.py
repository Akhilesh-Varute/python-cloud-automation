import sys
import csv
from collections import Counter


def count_words(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().lower().split()
    return Counter(text)


def save_words_count_to_csv(counts, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        for word, cnt in counts.items():
            writer.writerow([word, cnt])


def main():
    if len(sys.argv) != 3:
        print("Usage: python word_count.py input.txt output.csv")
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]
    counts = count_words(input_path)
    save_words_count_to_csv(counts, output_path)
    print(f"Processed {len(counts)} unique words -> saved to {output_path}")


if __name__ == "__main__":
    main()
