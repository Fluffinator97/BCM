SIGNALS = {
    # Engine
    0x100: {"system": "engine", "display": True, "display_order": 1, "signal": "Engine RPM", "bytes": 2, "scale": 1, "warning_max": 7500, "critical_max": 8500, "unit": "rpm"},
    0x101: {"system": "engine", "display": True, "display_order": 2, "signal": "Engine Coolant Temperature", "bytes": 1, "scale": 1, "warning_max": 105, "critical_max": 115, "unit": "C"},
    0x102: {"system": "engine", "display": True, "display_order": 3, "signal": "Engine Air Intake Temperature", "bytes": 1, "scale": 1, "warning_max": 60, "critical_max": 80, "unit": "C"},
    0x103: {"system": "engine", "display": True, "display_order": 4, "signal": "Throttle Position", "bytes": 1, "scale": 1, "unit": "%"},
    0x104: {"system": "engine", "display": True, "display_order": 5, "signal": "Air Fuel Ratio", "bytes": 2, "scale": 0.1, "warning_min": 10.0, "warning_max": 16.0, "critical_min": 9.0, "critical_max": 18.0, "unit": "afr"},
    0x105: {"system": "engine", "display": True, "display_order": 6, "signal": "Ignition Timing", "bytes": 2, "scale": 0.1, "unit": "deg"},
    0x106: {"system": "engine", "display": True, "display_order": 7, "signal": "Ignition Correction", "bytes": 2, "scale": 0.1, "signed": True, "warning_min": -4, "critical_min": -8, "unit": "deg"},
    0x107: {"system": "engine", "display": True, "display_order": 8, "signal": "Engine Load", "bytes": 1, "scale": 1, "warning_max": 95, "critical_max": 100, "unit": "%"},
    0x108: {"system": "engine", "display": True, "display_order": 9, "signal": "Lambda", "bytes": 2, "scale": 0.001, "warning_min": 0.75, "warning_max": 1.20, "critical_min": 0.65, "critical_max": 1.40, "unit": "lambda"},
    0x109: {"system": "engine", "display": True, "display_order": 10, "signal": "Knock Count", "bytes": 1, "scale": 1, "warning_max": 3, "critical_max": 6, "unit": "count"},

    # Oil
    0x200: {"system": "oil", "display": True, "display_order": 11, "signal": "Oil Pressure", "bytes": 1, "scale": 1, "warning_min": 25, "critical_min": 10, "unit": "psi"},
    0x201: {"system": "oil", "display": True, "display_order": 12, "signal": "Oil Temperature", "bytes": 1, "scale": 1, "warning_max": 120, "critical_max": 135, "unit": "C"},
    0x202: {"system": "oil", "display": True, "display_order": 13, "signal": "Oil Level", "bytes": 1, "scale": 1, "warning_min": 20, "critical_min": 10, "unit": "%"},
    0x203: {"system": "oil", "display": True, "display_order": 14, "signal": "Accusump Pressure", "bytes": 1, "scale": 1, "warning_min": 20, "critical_min": 10, "unit": "psi"},

    # Turbo
    0x300: {"system": "turbo", "display": True, "display_order": 15, "signal": "Turbo Boost Pressure", "bytes": 2, "scale": 0.1, "signed": True, "warning_max": 28, "critical_max": 35, "unit": "psi"},
    0x301: {"system": "turbo", "display": True, "display_order": 16, "signal": "Turbo Wastegate Duty", "bytes": 1, "scale": 1, "warning_max": 90, "critical_max": 100, "unit": "%"},
    0x302: {"system": "turbo", "display": True, "display_order": 17, "signal": "Turbo Shaft Speed", "bytes": 2, "scale": 100, "warning_max": 140000, "critical_max": 180000, "unit": "rpm"},
    0x303: {"system": "turbo", "display": True, "display_order": 18, "signal": "Charge Air Temperature", "bytes": 1, "scale": 1, "warning_max": 55, "critical_max": 75, "unit": "C"},

    # Cooling
    0x400: {"system": "cooling", "display": True, "display_order": 19, "signal": "Radiator Outlet Temperature", "bytes": 1, "scale": 1, "warning_max": 95, "critical_max": 110, "unit": "C"},
    0x401: {"system": "cooling", "display": True, "display_order": 20, "signal": "Cooling Fan Speed", "bytes": 2, "scale": 1, "unit": "rpm"},
    0x402: {"system": "cooling", "display": True, "display_order": 21, "signal": "Water Pump Speed", "bytes": 2, "scale": 1, "warning_min": 1000, "critical_min": 500, "unit": "rpm"},
    0x403: {"system": "cooling", "display": True, "display_order": 22, "signal": "Cooling Fan Duty", "bytes": 1, "scale": 1, "warning_max": 95, "critical_max": 100, "unit": "%"},

    # Transmission
    0x500: {"system": "transmission", "display": True, "display_order": 23, "signal": "Current Gear Position", "bytes": 1, "scale": 1, "unit": ""},
    0x501: {"system": "transmission", "display": True, "display_order": 24, "signal": "Transmission Temperature", "bytes": 1, "scale": 1, "warning_max": 105, "critical_max": 120, "unit": "C"},
    0x502: {"system": "transmission", "display": True, "display_order": 25, "signal": "Clutch Position", "bytes": 1, "scale": 1, "unit": "%"},
    0x503: {"system": "transmission", "display": True, "display_order": 26, "signal": "Differential Temperature", "bytes": 1, "scale": 1, "warning_max": 120, "critical_max": 140, "unit": "C"},

    # Electrical
    0x600: {"system": "electrical", "display": True, "display_order": 27, "signal": "Battery Voltage", "bytes": 2, "scale": 0.1, "warning_min": 12.0, "warning_max": 15.0, "critical_min": 11.0, "critical_max": 16.0, "unit": "V"},
    0x601: {"system": "electrical", "display": True, "display_order": 28, "signal": "Alternator Voltage", "bytes": 2, "scale": 0.1, "warning_min": 12.0, "warning_max": 15.0, "critical_min": 11.0, "critical_max": 16.0, "unit": "V"},
    0x602: {"system": "electrical", "display": True, "display_order": 29, "signal": "Current Draw", "bytes": 2, "scale": 0.1, "unit": "A"},

    # Alerts
    0x700: {"system": "alerts", "display": True, "display_order": 30, "signal": "Knock Alert Status", "bytes": 1, "enum": {0: "OK", 1: "Warning", 2: "Critical"}, "unit": ""},
    0x701: {"system": "alerts", "display": True, "display_order": 31, "signal": "Low Oil Pressure Alert", "bytes": 1, "enum": {0: "OK", 1: "Warning", 2: "Critical"}, "unit": ""},
    0x702: {"system": "alerts", "display": True, "display_order": 32, "signal": "Overboost Alert", "bytes": 1, "enum": {0: "OK", 1: "Warning", 2: "Critical"}, "unit": ""},
    0x703: {"system": "alerts", "display": True, "display_order": 33, "signal": "Overheat Alert", "bytes": 1, "enum": {0: "OK", 1: "Warning", 2: "Critical"}, "unit": ""},
    0x704: {"system": "alerts", "display": True, "display_order": 34, "signal": "Sensor Fault Alert", "bytes": 1, "enum": {0: "OK", 1: "Warning", 2: "Critical"}, "unit": ""},

    # Wheels
    0x800: {"system": "wheels", "display": True, "display_order": 35, "signal": "Front Left Wheel Speed", "bytes": 2, "scale": 0.1, "unit": "kmh"},
    0x801: {"system": "wheels", "display": True, "display_order": 36, "signal": "Front Right Wheel Speed", "bytes": 2, "scale": 0.1, "unit": "kmh"},
    0x802: {"system": "wheels", "display": True, "display_order": 37, "signal": "Rear Left Wheel Speed", "bytes": 2, "scale": 0.1, "unit": "kmh"},
    0x803: {"system": "wheels", "display": True, "display_order": 38, "signal": "Rear Right Wheel Speed", "bytes": 2, "scale": 0.1, "unit": "kmh"},

    # Stability / chassis
    0x900: {"system": "stability", "display": True, "display_order": 39, "signal": "Steering Angle", "bytes": 2, "scale": 0.1, "signed": True, "unit": "deg"},
    0x901: {"system": "stability", "display": True, "display_order": 40, "signal": "Yaw Rate", "bytes": 2, "scale": 0.1, "signed": True, "unit": "deg/s"},
    0x902: {"system": "stability", "display": True, "display_order": 41, "signal": "Lateral G Force", "bytes": 2, "scale": 0.01, "signed": True, "unit": "g"},
    0x903: {"system": "stability", "display": True, "display_order": 42, "signal": "Longitudinal G Force", "bytes": 2, "scale": 0.01, "signed": True, "unit": "g"},
    0x904: {"system": "stability", "display": True, "display_order": 43, "signal": "Brake Pressure Front", "bytes": 2, "scale": 0.1, "unit": "bar"},
    0x905: {"system": "stability", "display": True, "display_order": 44, "signal": "Brake Pressure Rear", "bytes": 2, "scale": 0.1, "unit": "bar"},

    # Combined alert state
    0xA00: {"system": "alerts", "display": True, "display_order": 45, "signal": "Alert Flags", "bytes": 1, "enum": {0: "OK", 1: "Warning", 2: "Critical"}, "unit": ""},
}