import csv
from pathlib import Path

from src.parser import parse_candump_line
from src.decoder import decode_basic

INPUT_LOG = Path("logs/sample.log")
OUTPUT_CSV = Path("out/telemetry.csv")

def main():
    OUTPUT_CSV.parent.mkdir(exist_ok=True)

    rows = []

    for line in INPUT_LOG.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        frame = parse_candump_line(line)
        decoded = decode_basic(frame)
        rows.append(decoded)

    with OUTPUT_CSV.open("w", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "timestamp",
                "interface",
                "can_id",
                "system",
                "signal",
                "raw_value",
                "value",
                "unit",
                "status",
                "data",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()