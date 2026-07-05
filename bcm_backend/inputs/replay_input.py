import time
from pathlib import Path
from bcm_backend.inputs.base import TelemetryInput
from bcm_can_parser.src.parser import parse_candump_line

BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_LOG = BASE_DIR / "bcm_can_parser" / "logs" / "sample.log"

class ReplayInput(TelemetryInput):
    def __init__(self, log_path=DEFAULT_LOG, speed=1.0):
        self.log_path = Path(log_path)
        self.speed = speed

    def load_frames(self):
        frames = []
        

        for line in self.log_path.read_text().splitlines():
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            frames.append(parse_candump_line(line))

        frames.sort(key=lambda frame: frame.timestamp)
        return frames
    
    def frames(self):
        loaded_frames = self.load_frames()
        print("loading from:", self.log_path)
        print("exists", self.log_path.exists())

        if not loaded_frames:
            print("no frames loaded")
            return
        
        previous_timestamp = loaded_frames[0].timestamp

        for index, frame in enumerate(loaded_frames):
            if index == 0:
                delay = 0
            else:
                delay = max(frame.timestamp - previous_timestamp, 0)

            if self.speed > 0:
                time.sleep(delay / self.speed)

            yield frame

            previous_timestamp = frame.timestamp