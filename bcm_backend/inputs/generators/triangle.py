import math
import random
from typing import Any

def generate_triangle_value(
        elapsed: float,
        profile: dict[str, Any]
) -> float:
    base = profile.get("base", 0)
    amplitude = profile.get("amplitude", 1)
    frequency = profile.get("frequency", 1)

    phase = (frequency * elapsed) % 1.0
    wave = 1 -4 * abs(phase - 0.5)

    return base + amplitude * wave