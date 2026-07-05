import { useEffect, useState } from "react";
import { getTelemerty, startTelemetry, hideSignal } from "../api/telemetryApi";

const SYSTEM_ORDER = [
  "engine",
  "oil",
  "turbo",
  "cooling",
  "transmission",
  "electrical",
  "wheels",
  "stability",
  "alerts",
  "unknown",
];

function groupTelemetry(data: any) {
  if (!data) return []

  return SYSTEM_ORDER
    .filter((system) => data[system])
    .map((system) => ({
      system,
      signals: Object.values(data[system]),
    }));
}

function statusClass(status: string) {
  const lower = status?.toLowerCase() ?? "";

  if (lower.includes("critical")) return "critical"
  if (lower.includes("warning")) return "warning"
  return "normal"
}



function DashboardPage() {
    const [data, setData] = useState<any>(null);

    useEffect(() => {
      const interval = setInterval(() => {
        getTelemerty().then(setData)
    }, 500);

    return () => clearInterval(interval)
  }, [])

    const groups = groupTelemetry(data)

  return (
    <main className="app">
      <header className="header">
        <div>
          <h1>BCM Telemetry</h1>
          <p>Live simulated CAN telemetry</p>
          <button onClick={() => startTelemetry()}>Start Replay</button>
        </div>
      </header>

      <div className="grid">
        {groups.map((group: any) => (
          <section className="system-card" key={group.system}>
            <h2>{group.system.toUpperCase()}</h2>

            <div className="signals">
              {group.signals.map((signal: any) => (
                <div className="signal-row" key={signal.signal}>
                  <div>
                    <span className="signal-name">{signal.signal}</span>
                    <span className="signal-status">{signal.status}</span>
                    <button onClick={async () => {
                        await hideSignal(
                            group.system, 
                            signal.signal
                        )
                        const updated = await getTelemerty();
                        setData(updated);
                        }}
                        >
                        Hide
                        </button>
                  </div>

                  <div className="value-block">
                    <span className={`lamp ${statusClass(signal.status)}`} />
                    <span className="value">{signal.value}</span>
                    <span className="unit"> {signal.unit}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>
    </main>
  );

};

export default DashboardPage;