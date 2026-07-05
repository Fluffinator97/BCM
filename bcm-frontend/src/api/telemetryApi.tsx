const API_BASE = "http://127.0.0.1:8000";

export async function getTelemerty() {
    const res = await fetch(`${API_BASE}/api/telemetry`);
    return res.json()
}

export async function getAllSignals() {
    const res = await fetch(`${API_BASE}/api/signals`)
    return res.json();
}

export async function startTelemetry() {
    const res = await fetch(`${API_BASE}/api/replay/start`,
        {
            method: "POST",
        }
    );
    return res.json()
}

export async function hideSignal(
    system: string,
    signal: string
) {
    const res = await fetch(`${API_BASE}/api/${system}/${signal}`,
        {
            method: "DELETE"
        }
    );
    return res.json();
};