import { useEffect, useState } from "react";
import { getAllSignals, hideSignal, showSignal } from "../api/telemetryApi";

function SignalsPage() {
    const [ signals, setSignals ] = useState<any>(null)

    useEffect(() => {
        getAllSignals().then(setSignals);
    }, []);

    return (
        <section>
            <h1>All Signals</h1>

            <div className="grid">
                {signals &&
                    Object.entries(signals).map(([canId, signal]: any ) =>
                    <div className="system-card" key={canId}>
                        <h2>{canId}</h2>
                        <p><strong>{signal.signal}</strong></p>
                        <p>System: {signal.system}</p>
                        <p>Bytes: {signal.bytes}</p>
                        <p>Scale: {signal.scale ?? "-"}</p>
                        <p>Unit: {signal.unit || "-"}</p>
                        <p>Display: {String(signal.visible ?? false)}</p>
                        <label className="switch">
                        <input
                            type="checkbox"
                            checked={signal.visible}
                            onChange={async () => {
                                if (signal.visible) {
                                    await hideSignal(signal.system, signal.signal);
                                } else {
                                    await showSignal(signal.system, signal.signal);
                                }
                                const updated = await getAllSignals();
                                setSignals(updated)
                            }}
                            />
                            <span className="slider" />
                            </label>
                    </div>
                    )}
            </div>
        </section>
    );
}

export default SignalsPage;