from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from bcm_backend.telemerty_runtime import set_broadcast_callback
from urllib.parse import unquote

from bcm_backend.telemerty_runtime import telemetry_state, start_replay
from bcm_backend.telemerty_runtime import (telemetry_history, telemetry_lock)
from bcm_backend.display_config import is_signal_visible, set_signal_visible
from bcm_backend.telemerty_runtime import start_mock

from bcm_can_parser.src.signals import SIGNALS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def broadcast_telemetry(data):
    await manager.broadcast({
        "type": "telemetry",
        "data": data,
    })

async def broadcast_history(
        system: str,
        signal: str,
        point: dict,
):
    await manager.broadcast({
        "type": "history",
        "data": {
            "system": system,
            "signal": signal,
            "point": point,
        }
    })


@app.on_event("startup")
async def store_event_loop():
    app.state.event_loop = asyncio.get_running_loop()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, data):
        dead_connections = []

        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception:
                dead_connections.append(connection)

        for connection in dead_connections:
            self.disconnect(connection)


manager = ConnectionManager()


loop = asyncio.get_event_loop()


def broadcast_from_thread(message: dict):
    asyncio.run_coroutine_threadsafe(
        manager.broadcast(message),
        app.state.event_loop,
    )

set_broadcast_callback(broadcast_from_thread)

@app.get("/")
def root():
    return {"message": "BCM CAN Backend Running"}



@app.websocket("/ws/telemetry")
async def telemetry_websocket(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)





hidden_signals = set()



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

@app.post("/api/mock/start")
def mock_start(update_rate_hz: float = 10.0):
    return start_mock(update_rate_hz)

@app.get("/api/telemetry/history/{system}/{signal_name}")
def get_signal_history(
    system: str,
    signal_name: str,
    limit: int = 300,
):
    if limit < 1 or limit > 5000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 5000"
        )
    
    with telemetry_lock:
        system_history = telemetry_history.get(system)

        if not system_history or signal_name not in system_history:
            raise HTTPException(
                status_code=404,
                detail="No history found for this signal",
            )
        values = list(system_history[signal_name])

        return {
            "system": system,
            "signal": signal_name,
            "count": min(limit, len(values)),
            "history": values[-limit:],
        }