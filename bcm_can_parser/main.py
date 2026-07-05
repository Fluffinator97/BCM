import sys
import json
from pathlib import Path

from src.parser import parse_candump_line
from src.decoder import decode_basic


def main(path: str) -> None:
    log_path = Path(path)
    if not log_path.exists():
        raise FileNotFoundError(log_path)

    for line in log_path.read_text().splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        frame = parse_candump_line(line)
        decoded = decode_basic(frame)
        print(json.dumps(decoded, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py logs/sample.log")
        raise SystemExit(1)

    main(sys.argv[1])
