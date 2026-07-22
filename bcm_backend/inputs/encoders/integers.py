def encode_u8(value: int) -> bytes:
    return int(value).to_bytes(1, "big") + bytes(7)

def encode_i8(value: int) -> bytes:
    return int(value).to_bytes(1, "big", signed=True) + bytes(7)


def encode_u16(value: int) -> bytes:
    return int(value).to_bytes(2, "big") + bytes(6)

def encode_i16(value: int) -> bytes:
    return int(value).to_bytes(2, "big", signed=True) + bytes(6)
