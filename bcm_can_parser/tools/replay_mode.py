import time
from pathlib import Path

from src.parser import parse_candump_line
from src.decoder import decode_basic

INPUT_LOG = Path("logs/sample.log")

def load_frames(path: Path):
    frames = []

    for line in path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        frames.append(parse_candump_line(line))

    return frames

def main():
    frames = load_frames(INPUT_LOG)
    
    if not frames:
        print("No frames found.")
        return
    
    previous_timestamp = frames[0].timestamp

    for frame in frames:
        delay = frame.timestamp - previous_timestamp

        if delay > 0:
            time.sleep(delay)

        decoded = decode_basic(frame)
        print(decoded)

        previous_timestamp = frame.timestamp

if __name__ == "__main__":
    main()