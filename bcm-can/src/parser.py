from dataclasses import dataclass


@dataclass(frozen=True)
class CANFrame:
    timestamp: float
    interface: str
    can_id: int
    data: bytes

    @property
    def dlc(self) -> int:
        return len(self.data)


def parse_candump_line(line: str) -> CANFrame:
    """Parse candump format: (timestamp) iface CANID#DATAHEX"""
    parts = line.strip().split()
    if len(parts) != 3:
        raise ValueError(f"Invalid candump line: {line!r}")

    ts_part, interface, frame_part = parts

    if not ts_part.startswith("(") or not ts_part.endswith(")"):
        raise ValueError(f"Invalid timestamp: {ts_part!r}")

    if "#" not in frame_part:
        raise ValueError(f"Missing # separator: {frame_part!r}")

    timestamp = float(ts_part.strip("()"))
    can_id_hex, data_hex = frame_part.split("#", 1)

    if len(data_hex) % 2 != 0:
        raise ValueError(f"Data hex must have even length: {data_hex!r}")

    return CANFrame(
        timestamp=timestamp,
        interface=interface,
        can_id=int(can_id_hex, 16),
        data=bytes.fromhex(data_hex),
    )
