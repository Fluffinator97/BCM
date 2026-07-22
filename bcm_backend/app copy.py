from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import unquote

from bcm_backend.telemerty_runtime import telemetry_state, start_replay
from bcm_backend.display_config import is_signal_visible, set_signal_visible

from bcm_can_parser.src.signals import SIGNALS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

hidden_signals = set()


@app.get("/")
def root():
    return {"message": "BCM CAN Backend Running"}

@app.get("/api/telemetry")
def get_telemetry():
    filtered = {}

    for system, signals in telemetry_state.items():
        for signal_name, data in signals.items():
            if not is_signal_visible(system, signal_name):
                continue

            filtered.setdefault(system, {})
            filtered[system][signal_name] = data
    return filtered

@app.post("/api/replay/start")
def replay_start():
    start_replay(speed=1.0)
    return {"status": "replay started"}


@app.get("/api/debug")
def debug():
    from telemerty_runtime import INPUT_LOG, is_running
    return {
        "input_log": str(INPUT_LOG.resolve()),
        "log_exists": INPUT_LOG.exists(),
        "is_running": is_running,
        "start_size": len(telemetry_state),
    }

@app.get("/api/signals")
def get_signals():
    return {
        f"0x{can_id:x}": {
            **definition,
            "visible": is_signal_visible(
                definition["system"],
                definition["signal"]
            )
        }
        for can_id, definition in SIGNALS.items()
    }

@app.delete("/api/signals/{system}/{signal_name}")
def hide_signal(system: str, signal_name: str):
    print("DELETE called:", system, signal_name)

    result = set_signal_visible(system, signal_name, False)
    print("Result:", result)
    return result

@app.post("/api/signals/{system}/{signal_name}/show")
def show_signal(system: str, signal_name: str):
    signal_name = unquote(signal_name)
    return set_signal_visible(system,signal_name, True)


@app.get("/api/debug/display-config")
def debug_display_config():
    from display_config import CONFIG_PATH, load_display_config

    return {
        "config_path": str(CONFIG_PATH),
        "exists": CONFIG_PATH.exists(),
        "content": load_display_config(),
    }
