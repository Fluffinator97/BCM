from bcm_can_parser.src.parser import CANFrame
from bcm_can_parser.src.signals import SIGNALS


def decode_basic(frame: CANFrame) -> dict:
    """Generic decoded representation. Later, replace with car-specific signal decoding."""
    definition = SIGNALS.get(frame.can_id)

    if definition is None:
        return {
            "timestamp": frame.timestamp,
            "interface": frame.interface,
            "system": "unknown",
            "signal": f"Unknown CAN ID 0x{frame.can_id:X}",
            "raw_value": None,
            "value": None,
            "unit": "",
            "status": "unknown: No definition for this CAN ID",
            "can_id_hex": f"0x{frame.can_id:X}",
            "data": frame.data.hex().upper(),
        }
    
    byte_count = definition["bytes"]
    scale = definition.get("scale", 1)
    offset = definition.get("offset", 0)
    enum_map = definition.get("enum")

    signed = definition.get("signed", False)


    raw_value = int.from_bytes(frame.data[0:byte_count], "big", signed=signed)

    if enum_map:
        value = enum_map.get(raw_value, f"Unknown ({raw_value})")
    else: 
        value = raw_value * scale + offset
        
    def validate_value(value, definition):
        if "critical_min" in definition:
            if value < definition["critical_min"]:
                return "critical: Operating below critical limit"
        if "critical_max" in definition:
            if value > definition["critical_max"]:
                return "critical: Operating above critical limit"
        if "warning_min" in definition:
            if value < definition["warning_min"]:
                return "warning: Operating below warning limit"
        if "warning_max" in definition:
            if value > definition["warning_max"]:
                return "warning: Operating above warning limit"

        return "normal: Operating within normal limits"
    
    status = validate_value(value, definition)


    return {
        "timestamp": frame.timestamp,
        "interface": frame.interface,
        "system": definition["system"],
        "signal": definition["signal"],
        "status": status,
        "raw_value": raw_value,
        "value": value,
        "unit": definition["unit"],
        "can_id": frame.can_id,
        "data": frame.data.hex(),
    }