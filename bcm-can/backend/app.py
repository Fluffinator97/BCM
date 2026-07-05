from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.telemerty_runtime import telemetry_state, start_replay

from src.signals import SIGNALS

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
            if (system, signal_name) in hidden_signals:
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
    from backend.telemerty_runtime import INPUT_LOG, is_running
    return {
        "input_log": str(INPUT_LOG.resolve()),
        "log_exists": INPUT_LOG.exists(),
        "is_running": is_running,
        "start_size": len(telemetry_state),
    }

@app.get("/api/signals")
def get_signals():
    return {
        f"0x{can_id:x}": definition
        for can_id, definition in SIGNALS.items()
    }

@app.delete("/api/signals/{system}/{signal_name}")
def hide_signal(system: str, signal_name: str):
    hidden_signals.add((system, signal_name))
    return {"status": "hidden", "system": system, "signal": signal_name}

