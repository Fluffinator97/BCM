import json
from pathlib import Path

SIGNALS_PATH = Path(__file__).resolve().parent.parent.parent / "bcm_backend" / "config" / "signals.json"

def load_signals():
    raw = json.loads(SIGNALS_PATH.read_text())

    return {
        int(can_id, 16): definition
        for can_id, definition in raw.items()
    }

SIGNALS = load_signals()