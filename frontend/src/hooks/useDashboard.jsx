import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;
const POLL_MS = 2000;

export function useDashboard() {
  const [latest,   setLatest]   = useState(null);
  const [history,  setHistory]  = useState([]);
  const [stats,    setStats]    = useState(null);
  const [online,   setOnline]   = useState(false);
  const [lastPoll, setLastPoll] = useState(null);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [latestRes, historyRes, statsRes] = await Promise.all([
          fetch("${API_URL}/api/latest"),
          fetch("${API_URL}/api/history?limit=30"),
          fetch("${API_URL}/api/stats"),
        ]);

        if (latestRes.ok) {
          const data = await latestRes.json();
          if (!data.error) {
            setLatest(data);
            setOnline(true);
          }
        } else {
          setOnline(false);
        }

        if (historyRes.ok) {
          const data = await historyRes.json();
          setHistory(data);
        }

        if (statsRes.ok) {
          const data = await statsRes.json();
          setStats(data);
        }

        setLastPoll(new Date().toLocaleTimeString());
      } catch {
        setOnline(false);
      }
    };

    fetchAll();
    const id = setInterval(fetchAll, POLL_MS);
    return () => clearInterval(id);
  }, []);

  return { latest, history, stats, online, lastPoll };
}