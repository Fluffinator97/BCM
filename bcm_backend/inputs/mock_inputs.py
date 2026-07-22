import math
import random
import time

from bcm_backend.inputs.base import TelemetryInput
from bcm_can_parser.src.parser import CANFrame


class MockInput(TelemetryInput):
    def __init__(self, update_rate_hz: float = 10.0):
        if update_rate_hz <= 0:
            raise ValueError("update_rate_hz must be greater than zero")
        
        self.update_rate_hz = update_rate_hz
        self.running = True

    def stop(self):
        self.running = False
    
    def frames(self):
        start_time = time.time()
        interval = 1 / self.update_rate_hz

        while self.running:
            now = time.time()
            elapsed = now - start_time

            rpm = 2500 + 1500 * math.sin(elapsed)
            rpm += random.uniform(-60, 60)

            raw_rpm = max(0, round(rpm))
            data = raw_rpm.to_bytes(2, "big") + bytes(8)

            yield CANFrame(
                timestamp=now,
                interface="mock0",
                can_id=0x100,
                data=data,
            )

            time.sleep(interval)

