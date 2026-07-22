import threading
from collections import defaultdict, deque
from threading import Lock
from typing import Any

from bcm_backend.inputs.replay_input import ReplayInput
from bcm_can_parser.src.decoder import decode_basic
from bcm_backend.inputs.mock_inputs import MockInput

telemetry_state = {}
is_running = False

active_inputs = {}
input_threads = {}


broadcast_callback = None

HISTORY_LIMIT = 1000

telemetry_state: dict[str, dict[str, dict[str, Any]]] = {}

telemetry_history: dict[
    str,
    dict[str, deque[dict[str, any]]]
] = defaultdict(
    lambda: defaultdict(
        lambda: deque(maxlen=HISTORY_LIMIT)
    )
)

telemetry_lock = Lock()

def set_broadcast_callback(callback):
    global broadcast_callback
    broadcast_callback = callback

def run_input(name: str, input_source):
    try:
        for frame in input_source.frames():
            decoded = decode_basic(frame)

            system = decoded.get("system")
            signal = decoded.get("signal")

            if not system or not signal:
                continue

            history_point = {
                "timestamp": decoded["timestamp"],
                "value": decoded["value"],
                "status": decoded.get("status", "Normal"),
            }
                
            with telemetry_lock:
                telemetry_state.setdefault(system, {})
                telemetry_state[system][signal] = decoded

                telemetry_history[system][signal].append(history_point)


            if broadcast_callback:
                broadcast_callback({
                    "type": "telemetry",
                    "data": telemetry_state,
                    })
                
            if broadcast_callback:
                broadcast_callback({
                    "type": "history",
                    "data": {
                        "system": system,
                        "signal": signal,
                        "point": history_point
                    }
                })

    finally: 
        active_inputs.pop(name, None)
        input_threads.pop(name, None)


active_input = None
input_thread = None

def start_input(name: str, input_source):
    if name in active_inputs:
        return {
            "status": "already running",
            "input": name,
        }
    
    active_inputs[name] = input_source
    
    thread = threading.Thread(
        target=run_input,
        args=(name, input_source,),
        daemon=True,
    )

    input_threads[name] = thread
    thread.start()


    return {"status": "started", "input": name}

def start_replay(speed = 1.0):
    return start_input("replay", ReplayInput(speed=speed))

def start_mock(update_rate_hz=10.0):
    return start_input("mock", MockInput(update_rate_hz=update_rate_hz))

def start_replay_old(speed=1.0):
    global is_running

    if is_running:
        return {"Status": "already running"}
    
    input_source = ReplayInput(speed=speed)

    thread = threading.Thread(
        target = run_input,
        args = (input_source,),
        daemon=True,
    )
    thread.start()

    return {"status": "replay started", "speed": speed }