from pathlib import Path
BACKEND_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BACKEND_DIR / "config"

DISPLAY_CONFIG_PATH = CONFIG_DIR / "display_config.json"
SIGNALS_CONFIG_PATH = CONFIG_DIR / "signals.json"