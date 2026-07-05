import { useState } from "react";
import DashboardPage from "./pages/DashboardPage";
import SignalsPage from "./pages/SignalsPage"
import "./App.css"

function App() {
  const [ page, setPage ] = useState<"dashboard" | "signals">("dashboard");

  return (
    <main className="app">
      <nav className="nav">
        <button onClick={() => setPage("dashboard")}>Dashboard</button>
        <button onClick={() => setPage("signals")}>Signals</button>
      </nav>

      { page === "dashboard" && <DashboardPage /> }
      { page === "signals" && <SignalsPage /> }
    </main>
  );
}

export default App;