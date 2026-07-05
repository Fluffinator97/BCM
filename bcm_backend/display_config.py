import json
from pathlib import Path

from bcm_backend.config_paths import DISPLAY_CONFIG_PATH

CONFIG_PATH = DISPLAY_CONFIG_PATH

def load_display_config():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(exist_ok=True)
        CONFIG_PATH.write_text("{}")

    return json.loads(CONFIG_PATH.read_text())

def save_display_config(config):
    CONFIG_PATH.parent.mkdir(exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2))

def make_signal_key(system, signal):
    return f"{system}:{signal}"

def is_signal_visible(system, signal):
    config = load_display_config()
    key = make_signal_key(system, signal)

    return config.get(key, True)

def set_signal_visible(system, signal, visible):
    config = load_display_config()
    key = f"{system}:{signal}"

    config[key] = visible

    save_display_config(config)

    return {
        "system": system,
        "signal": signal,
        "visible": visible,
        "key": key
    }

