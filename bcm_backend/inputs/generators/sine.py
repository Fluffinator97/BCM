import math
import random
from typing import Any

def generate_sine_value(
    elapsed: float,
    profile: dict[str, Any]
) -> float:
    base = profile.get("base", 0)
    amplitude = profile.get("amplitude", 1)
    frequency = profile.get("frequency", 1)
    noise = profile.get("noise", 0)

    value = (
        base
        + amplitude * math.sin(2 * math.pi * frequency * elapsed)
        + random.uniform(-noise, noise)
    )

    ## minimum = profile.get("min")
    ## maximum = profile.get("max")

    ## if minimum is not None:
    ##    value = max(value, minimum)

    ## if maximum is not None:
    ##    value = min(value, maximum)

    
    return value