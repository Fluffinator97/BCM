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
    const res = await fetch(`${API_BASE}/api/signals/${system}/${signal}`,
        {
            method: "DELETE"
        }
    );
    return res.json();
};

export async function showSignal(
    system: string,
    signal: string
) {
    const res = await fetch(`${API_BASE}/api/signals/${system}/${signal}/show`,
        {
            method: "POST"
        }
    );
    return res.json();
};

export async function getSignalHistory(
    system: string,
    signal: string,
    limit: 300,
) {
    const url =
        `${API_BASE}/api/telemetry/history/` +
        `${encodeURIComponent(system)}/` +
        `${encodeURIComponent(signal)}` +
        `?limit=${limit}`

    const response = await fetch(url)

    if (!response.ok) {
        if (response.status === 404) {
            return {
                system,
                signal,
                history: [],
            };
        }

        throw new Error(`Failed to load signal history: ${response.status}`);
    }

    return response.json();
}