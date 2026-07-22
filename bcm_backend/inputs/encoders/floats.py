def encode_float16(value: float) -> bytes:
    return float(value).to_bytes(2, "big") + bytes(6)

def encode_ifloat16(value: float) -> bytes:
    return float(value).to_bytes(2, "big", signed=True) + bytes(6)