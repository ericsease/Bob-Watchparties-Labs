import { useState, useEffect } from "react";
import RepoList from "./components/RepoList";
import Sidebar from "./components/Sidebar";

export default function App() {
  const [repos, setRepos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/repos")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch repos");
        return res.json();
      })
      .then((data) => {
        setRepos(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="page-wrapper">
      <header>
        <h1>📡 RepoRadar</h1>
        <p>Trending open-source repos — updated daily</p>
      </header>

      {loading && <p className="state-message">Loading repos…</p>}
      {error && <p className="state-message">Error: {error}</p>}

      {!loading && !error && (
        <div className="app-shell">
          <Sidebar />
          <div className="main-content">
            <RepoList repos={repos} />
          </div>
        </div>
      )}
    </div>
  );
}
