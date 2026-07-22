const SOCKET_URL = "ws://127.0.0.1:8000/ws"

export type TelemetrySocketMessage =
    | {
        type: "telemetry";
        data: Record<string, unknown>
    }
    | {
        type: "history";
        data: {
            system: string;
            signal: string;
            point: {
                timestamp: number;
                value: number;
                status?: string;
            };
        };
    };


export function connectTelemetrySocket(
    onMessage: (message: TelemetrySocketMessage) => void
) {
    const socket = new WebSocket(`${SOCKET_URL}/telemetry`);

    socket.onmessage = (event) => {
        const message = JSON.parse(event.data) as TelemetrySocketMessage;
        onMessage(message);
    };

    socket.onopen = () => {
        console.log("Telemetry socket connected");
    };

    socket.onclose = () => {
        console.log("Telemetry socket disconnected");
    };

    return socket;
}