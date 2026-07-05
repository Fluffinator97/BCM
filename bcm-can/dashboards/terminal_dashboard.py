import os 
import time
import argparse
from pathlib import Path

from datetime import datetime

from src.parser import parse_candump_line
from src.decoder import decode_basic
from src.signals import SIGNALS

INPUT_LOG = Path("logs/sample.log")

parser = argparse.ArgumentParser()
parser.add_argument("--speed", type=float, default=1.0, help="Replay speed multiplier (default: 1.0)")

args = parser.parse_args()

replay_speed = args.speed

SYSTEM_ORDER = [
    "engine",
    "oil",
    "turbo",
    "cooling",
    "transmission",
    "electrical",
    "wheels",
    "stability",
    "alerts",
    "unknown"
]

def format_timestamp(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%H:%M:%S.%f")[:-3]  # Format to milliseconds

def get_display_signals():
    items = []

    for can_id, definition in SIGNALS.items():
        if definition.get("display", False):
                items.append({
                    "system": definition["system"],
                    "signal": definition["signal"],
                    "order": definition.get("display_order", 9999)
                })

    return sorted(
        items,
        key=lambda item: (
            SYSTEM_ORDER.index(item["system"])
            if item["system"] in SYSTEM_ORDER
            else 9999,
            item["order"]
        )
    )

def load_frames(path: Path):
    frames = []
    frames.sort(key=lambda frame: frame.timestamp)  # Sort frames by timestamp

    for line in path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        frames.append(parse_candump_line(line))

    return frames

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def format_value(entry):
    if entry is None:
        return "---"
    
    value = entry.get("value")
    unit = entry.get("unit", "")
    status = entry.get("status", "Normal")
    updated = format_timestamp(entry.get("timestamp"))

    if "Normal" in status or "normal" in status:
        status = ""

    if isinstance(value, float):
        value = round(value, 3)

    def status_lamp(status):
        if "Warning" in status or "warning" in status:
            return "\033[93m●\033[0m"  # Yellow
        elif "Critical" in status or "critical" in status:
            return "\033[91m●\033[0m"  # Red
        else:
            return "\033[92m●\033[0m"  # Green
        
    lamp = status_lamp(status)

    return f"{lamp} | {value} {unit} | {status} | Last Updated: {updated}"

def draw_dashboard(state):
    clear_screen()

    print("BCM TELEMETRY DASHBOARD")
    print("=" * 60)

    current_system = None

    for item in get_display_signals():
        system = item["system"]
        signal = item["signal"]

        if system != current_system:
            current_system = system
            print("-" * 60)
            print(f"\n[{system.upper()}]")
            print("-" * 60)

        entry = state.get(system, {}).get(signal)
        print(f"{signal:<32}: {format_value(entry)}")

    print("=" * 60)
    print("Press Ctrl+C to exit.")

def main():
    frames = load_frames(INPUT_LOG)

    if not frames:
        print("No frames found.")
        return
    
    state = {}
    
    previous_timestamp = frames[0].timestamp

    try:            
        for frame in frames:
            delay = frame.timestamp - previous_timestamp

            delay = max(delay, 0)  # Ensure non-negative delay


            if replay_speed > 0:
                time.sleep(delay / replay_speed)

            decoded = decode_basic(frame)

            signal = decoded.get("signal")
            system = decoded.get("system")

            if system and signal:
                state.setdefault(system, {})
                state[system][signal] = decoded

            draw_dashboard(state)

            previous_timestamp = frame.timestamp

    except KeyboardInterrupt:
        print("\nStopped dashboard.")

if __name__ == "__main__":
    main()