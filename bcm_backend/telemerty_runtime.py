import threading

from bcm_backend.inputs.replay_input import ReplayInput
from bcm_can_parser.src.decoder import decode_basic

telemetry_state = {}
is_running = False

def run_input(input_source):
    global is_running

    is_running = True

    for frame in input_source.frames():
        decoded = decode_basic(frame)

        system = decoded.get("system")
        signal = decoded.get("signal")

        if system and signal:
            telemetry_state.setdefault(system, {})
            telemetry_state[system][signal] = decoded

    is_running = False


def start_replay(speed=1.0):
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