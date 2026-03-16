import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "./Navbar";

const Analytics = ({ refreshTrigger }) => {
  const [summary, setSummary] = useState([]);
  const [period, setPeriod] = useState("today");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchAnalytics = async () => {
      setLoading(true);
      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/analytics/summary?period=${period}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );
        setSummary(response.data);
      } catch (err) {
        console.error("Failed to fetch analytics", err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, [period, refreshTrigger]);

  return (
    <main className="container">
      <Navbar />
      <article>
        <header>
          <nav>
            <ul>
              <li>
                <h4>Trends</h4>
              </li>
            </ul>
            <ul>
              <li>
                <button
                  className={period === "today" ? "" : "outline"}
                  onClick={() => setPeriod("today")}
                >
                  Today
                </button>
              </li>
              <li>
                <button
                  className={period === "7days" ? "" : "outline"}
                  onClick={() => setPeriod("7days")}
                >
                  7 Days
                </button>
              </li>
              <li>
                <button
                  className={period === "all" ? "" : "outline"}
                  onClick={() => setPeriod("all")}
                >
                  All Time
                </button>
              </li>
            </ul>
          </nav>
        </header>

        <div aria-busy={loading}>
          {summary.length === 0 && !loading ? (
            <p>No data for this period.</p>
          ) : (
            summary.map((item) => (
              <div key={item.label} style={{ marginBottom: "1rem" }}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    fontSize: "0.875rem",
                    marginBottom: "4px",
                  }}
                >
                  <strong style={{ textTransform: "capitalize" }}>
                    {item.label}
                  </strong>
                  <span>
                    {item.total_minutes} mins ({item.percentage}%)
                  </span>
                </div>
                <progress value={item.percentage} max="100" />
              </div>
            ))
          )}
        </div>
      </article>
    </main>
  );
};

export default Analytics;
