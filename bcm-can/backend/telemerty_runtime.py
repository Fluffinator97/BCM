import threading
import time
from pathlib import Path

from src.parser import parse_candump_line
from src.decoder import decode_basic


INPUT_LOG = Path("logs/sample.log")

telemetry_state = {}
is_running = False

def load_frames():
    frames = []

    for line in INPUT_LOG.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        frames.append(parse_candump_line(line))

    frames.sort(key=lambda frame: frame.timestamp)
    return frames

def replay_loop(speed=1.0):
    global is_running

    print("Replay loop started")

    frames = load_frames()
    print(f"Loaded {len(frames)} frames")

    if not frames:
        print("No frames loaded")
        return
    
    is_running = True
    previous_timestamp = frames[0].timestamp

    for index, frame in enumerate(frames):
        print(f"Frame {index}: {frame}")

        if index == 0:
            delay = 0
        else:
            delay = max(frame.timestamp - previous_timestamp, 0)

        if speed > 0:
            time.sleep(delay / speed)

        decoded = decode_basic(frame)
        print("Decoded:", decoded)

        system = decoded.get("system")
        signal = decoded.get("signal")

        if system and signal:
            telemetry_state.setdefault(system, {})
            telemetry_state[system][signal] = decoded
            print("state updated", system, signal)

        previous_timestamp = frame.timestamp

    is_running = False
    print("Replay lopp finished")


def start_replay(speed=1.0):
    if is_running:
        return
    
    thread = threading.Thread(
        target=replay_loop,
        kwargs={"speed": speed},
        daemon=True,
    )

    thread.start()