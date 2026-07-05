import { useEffect, useState } from "react";
import { getAllSignals } from "../api/telemetryApi";

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
                        <p>Display: {String(signal.display ?? false)}</p>
                    </div>
                    )}
            </div>
        </section>
    );
}

export default SignalsPage;