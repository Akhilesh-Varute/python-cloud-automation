import sys, csv
from collections import Counter


def count_characters(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().lower()
    return Counter(text)


def save_char_count_to_csv(counts, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["character", "count"])
        for char, cnt in counts.items():
            writer.writerow([char, cnt])


def main():
    if len(sys.argv) != 3:
        print("Usaeg char_count.py input.txt output.csv")
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]
    counts = count_characters(input_path)
    save_char_count_to_csv(counts, output_path)
    print(f"Processed {len(counts)} unique chars -> saved to {output_path}")


if __name__ == "__main__":
    main()
