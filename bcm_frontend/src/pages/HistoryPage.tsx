import {useEffect, useMemo, useState } from 'react';
import SignalChart from "../components/charts/SignalChart"
import { getAllSignals, getSignalHistory, startTelemetry } from "../api/telemetryApi";
import { connectTelemetrySocket } from '../api/telemetrySocket';

interface SignalDefinition {
    system: string;
    signal: string;
    unit?: string;
}

interface HistoryPoint {
    timestamp: number;
    value: number;
    status?: string;
}

interface HistoryMessage {
    type: "history";
    data: {
        system: string;
        signal: string;
        point: HistoryPoint;
    };
}

function HistoryPage() {
    const [signals, setSignals] = useState<Record<string, SignalDefinition>>({});
    const [selectedSystem, setSelectedSystem] = useState("");
    const [selectedSignal, setSelectedSignal] = useState("");
    const [history, setHistory] = useState<HistoryPoint[]>([]);

    useEffect(() => {
        getAllSignals().then((data) => {
            setSignals(data)
        })
    }, []);

    const systems = useMemo(() => {
        return Array.from(
            new Set(
                Object.values(signals).map((definition) => definition.system),
            ),
        );
    }, [signals]);

    const signalsForSelectedSystem = useMemo(() => {
        return Object.values(signals).filter(
            (definition) => definition.system === selectedSystem,
        );
    }, [signals, selectedSystem])

    function handleSystemChange(system: string) {
        setSelectedSystem(system);
        setSelectedSignal("");
        setHistory([]);
    }

    useEffect(() => {
        if (!selectedSystem || !selectedSignal) {
            setHistory([]);
            return;
        }

        getSignalHistory(selectedSystem, selectedSignal, 300)
            .then((response) => {
                setHistory(response.history);
            })
            .catch((error) => {
                console.error(error);
                setHistory([]);
            });
    }, [selectedSystem, selectedSignal]);

    useEffect(() => {
        const socket = connectTelemetrySocket((message) => {
            if (message.type !== "history") {
                return;
            }

            const historyMessage = message as HistoryMessage;
            const { system, signal, point } = historyMessage.data;

            if (
                system !== selectedSystem ||
                signal !== selectedSignal
            ) {
                return;
            }

            setHistory((currentHistory) => {
                const updatedHistory = [...currentHistory, point];

                return updatedHistory.slice(-300);
            });
        });
        return () => { socket.close(); };
    }, [selectedSystem, selectedSignal]);

    const selectedDefinition = signalsForSelectedSystem.find(
        (definition) => definition.signal === selectedSignal,
    );

    return (
        <main className='history-page'>
            <header>
                <h1>Telemetry History</h1>
                <p>Selected a signal to inspect its recent values</p>
                <button onClick={() => startTelemetry()}>Start Replay</button>
            </header>

            <div className='history-controls'>
                <label>
                    System
                    <select
                        value={selectedSystem}
                        onChange={(event) => handleSystemChange(event.target.value)}>
                            <option value="">Select system</option>
                            {systems.map((system) => (
                                <option key={system} value={system}>
                                    {system}
                                </option>
                            ))}
                    </select>
                </label>

                <label>
                    Signal
                    <select
                        value={selectedSignal}
                        disabled={!selectedSystem}
                        onChange={(event) => setSelectedSignal(event.target.value)}>
                            <option value="">Select signal</option>
                            {signalsForSelectedSystem.map((definition) => (
                                <option key={definition.signal} value={definition.signal}>
                                    {definition.signal}
                                </option>
                            ))}
                        </select>
                </label>
            </div>

            {selectedSignal ? (
                <SignalChart
                    signal={selectedSignal}
                    system={selectedSystem}
                    unit={selectedDefinition?.unit ?? ""}
                    history={history}
                    />
            ) : (
                <div className='empty-chart'>
                    Select a system and signal to display its history
                </div>
            )}
        </main>
    );
}

export default HistoryPage;