import Heatmap from "../components/Heatmap";
import EntryForm from "../components/EntryForm";
import VelocityChart from "../components/VelocityChart";
import { useEffect, useState } from "react";
import API from "../api";

export default function Dashboard() {
  const [streak, setStreak] = useState(0);
  const [velocity, setVelocity] = useState(0);
  const [consistency, setConsistency] = useState(0);
  const [refreshKey, setRefreshKey] = useState(0);
  const [trendData, setTrendData] = useState(0);

  const refresh = () => {
    setRefreshKey((prev) => prev + 1);
  };

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const [streakRes, velocityRes, consistencyRes, trendRes] =
          await Promise.all([
            API.get("/learning/analytics/streak"),
            API.get("/learning/analytics/velocity"),
            API.get("/learning/analytics/consistency"),
            API.get("/learning/analytics/velocity-trend"),
          ]);

        setStreak(streakRes.data.weekly_streak);
        setVelocity(velocityRes.data.weekly_average_hours_last_4_weeks);
        setConsistency(consistencyRes.data.consistency_score_percent);
        setTrendData(trendRes.data);
      } catch (err) {
        console.error("Analytics error:", err);
      }
    };

    fetchAnalytics();
  }, [refreshKey]);

  return (
    <div>
      <h1>Dashboard</h1>
      <section>
        <h2>Analytics</h2>
        <p>
          <strong>Weekly streak: </strong>
          {streak} weeks
        </p>
        <p>
          <strong>Learning Velocity: </strong>
          {streak} hrs/week
        </p>
        <p>
          <strong>Consistency (30 days): </strong>
          {consistency} %
        </p>
      </section>

      <VelocityChart data={trendData} />

      <EntryForm refresh={refresh} />
      <Heatmap key={refreshKey} />
    </div>
  );
}
