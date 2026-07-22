from typing import Any

def generate_square_value(
        elapsed: float,
        profile: dict[str, Any]
) -> float:
    frequency = profile.get("frequency", 1)
    low = profile.get("low", 0)
    high = profile.get("high", 1)

    phase = (frequency * elapsed) % 1.0

    return high if phase < 0.5 else low