import {
    CartesianGrid,
    Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts"

interface HistoryPoint {
    timestamp: number;
    value: number;
    status?: string
}

interface SignalChartProps {
    system: string;
    signal: string;
    unit?: string;
    history: HistoryPoint[];
}

interface ChartPoint extends HistoryPoint {
    elapsed: number;
    displayTime: string;
}

function SignalChart({
    system,
    signal,
    unit,
    history,
}: SignalChartProps) {
    const firstTimestamp = history[0]?.timestamp ?? 0;

    const chartData: ChartPoint[] = history.map((point) => ({
        ...point,
        elapsed: Number((point.timestamp - firstTimestamp).toFixed(2)),
        displayTime: new Date(point.timestamp * 1000).toLocaleTimeString(),
    }));

    return (
        <section className="chart-card">
            <div className="chart-header">
                <div>
                    <span className="chart-system">{system}</span>
                    <h2>{signal}</h2>
                </div>

                <span className="chart-count">
                    {history.length} points
                </span>
            </div>

            <div className="chart-container">
                <ResponsiveContainer width="100%" height={360}>
                    <LineChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3"/>

                        <XAxis
                            dataKey="elapsed"
                            type="number"
                            domain={["dataMin", "dataMax"]}
                            unit="s"
                        />

                        <YAxis
                            domain={["auto", "auto"]}
                            unit={unit ? `${unit}` : ""}
                            width={80}
                        />

                        <Tooltip
                            formatter={(value) => [
                                `${value} ${unit}`.trim(),
                                signal,
                            ]}
                            labelFormatter={(elapsed) => `${elapsed} seconds`}
                        />

                        <Line
                            type="monotone"
                            dataKey="value"
                            name={signal}
                            dot={false}
                            isAnimationActive={false}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </section>
    )

}

export default SignalChart;