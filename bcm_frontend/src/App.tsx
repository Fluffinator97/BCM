import { useState } from "react";
import DashboardPage from "./pages/DashboardPage";
import SignalsPage from "./pages/SignalsPage"
import HistoryPage from './pages/HistoryPage'
import "./App.css"

function App() {
  const [ page, setPage ] = useState<"dashboard" | "signals" | "history">("dashboard");

  return (
    <main className="app">
      <nav className="nav">
        <button onClick={() => setPage("dashboard")}>Dashboard</button>
        <button onClick={() => setPage("signals")}>Signals</button>
        <button onClick={() => setPage("history")}>History</button>
      </nav>

      { page === "dashboard" && <DashboardPage /> }
      { page === "signals" && <SignalsPage /> }
      { page === "history" && <HistoryPage />}
    </main>
  );
}

export default App;