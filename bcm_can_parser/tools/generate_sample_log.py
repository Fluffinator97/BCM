import json
from pathlib import Path
from src.signals import SIGNALS


def encode_value(value, byte_count, scale=1, offset=0, signed=False):
    raw_value = round((value - offset) / scale)

    return int(raw_value).to_bytes(byte_count, "big", signed=signed) + bytes(8 - byte_count)



def main():
    input_path = Path("data/mock_signals.json")
    output_path = Path("logs/sample.log")

    signals = json.loads(input_path.read_text())

    lines = []

    for item in signals:
        timestamp = float(item["timestamp"])
        interface = item.get("interface", "can0")
        can_id = int(item["id"], 16)
        signal = item["signal"]
        value = item["value"]

        definition = SIGNALS[can_id]

        byte_count = definition["bytes"]
        scale = definition.get("scale", 1)
        offset = definition.get("offset", 0)
        signed = definition.get("signed", False)
                                
        data = encode_value(value, byte_count, scale, offset, signed)

        lines.append(f"# {signal} ({can_id:X}) = {value}")
        lines.append(
            f"({timestamp:.6f}) {interface} {can_id:X}#{data.hex().upper()}"
        )

    output_path.write_text("\n".join(lines) + "\n")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()