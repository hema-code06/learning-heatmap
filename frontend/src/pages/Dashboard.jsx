import { useEffect, useState } from "react";
import API from "../api";
import DashboardLayout from "../layout/DashboardLayout";
import Card from "../components/ui/Card";
import EntryForm from "../components/EntryForm";
import VelocityChart from "../components/VelocityChart";
import TopicChart from "../components/TopicChart";
import GoalTracker from "../components/GoalTracker";
import CountUp from "react-countup";
import Skeleton from "../components/ui/skeleton";

import ProductivityCard from "../components/ProductivityCard";
import PatternCard from "../components/PatternCard";
import InsightsPanel from "../components/InsightsPanel";
import BadgePanel from "../components/BadgePanel";

export default function Dashboard() {
  const [streak, setStreak] = useState(0);
  const [velocity, setVelocity] = useState(0);
  const [consistency, setConsistency] = useState(0);
  const [refreshKey, setRefreshKey] = useState(0);
  const [trendData, setTrendData] = useState([]);
  const [topicData, setTopicData] = useState([]);
  const [advanced, setAdvanced] = useState(null);

  const refresh = () => setRefreshKey((prev) => prev + 1);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const [
          streakRes,
          velocityRes,
          consistencyRes,
          trendRes,
          topicRes,
          advancedRes,
        ] = await Promise.all([
          API.get("/learning/analytics/streak"),
          API.get("/learning/analytics/velocity"),
          API.get("/learning/analytics/consistency"),
          API.get("/learning/analytics/velocity-trend"),
          API.get("/learning/analytics/topic-breakdown"),
          API.get("/learning/analytics"),
        ]);

        setStreak(streakRes.data.weekly_streak);
        setVelocity(velocityRes.data.weekly_average_hours_last_4_weeks);
        setConsistency(consistencyRes.data.consistency_score_percent);
        setTrendData(trendRes.data);
        setTopicData(topicRes.data);
        setAdvanced(advancedRes.data);
      } catch (err) {
        console.error("Analytics error:", err);
      }
    };

    fetchAnalytics();
  }, [refreshKey]);

  return (
    <DashboardLayout>
      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-10">
        <MetricCard title="Weekly Streak" value={streak} suffix="weeks" />
        <MetricCard
          title="Learning Velocity"
          value={velocity}
          suffix="hrs/week"
        />
        <MetricCard title="Consistency Score" value={consistency} suffix="%" />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-10">
        <Card title="Weekly Learning Trend">
          {trendData.length === 0 ? (
            <Skeleton height="h-64" />
          ) : (
            <VelocityChart data={trendData} />
          )}
        </Card>

        <Card title="Topic Breakdown">
          <TopicChart data={topicData} />
        </Card>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-10">
        <Card title="Monthly Goal">
          <GoalTracker refreshKey={refreshKey} />
        </Card>

        <Card title="Add Learning Entry">
          <EntryForm refresh={refresh} />
        </Card>
      </div>
      {advanced && (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-10">
          <ProductivityCard data={advanced} />
          <PatternCard pattern={advanced.pattern} />
        </div>
      )}

      {advanced && (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-10">
          <InsightsPanel insights={advanced.insights} />
          <BadgePanel badges={advanced.badges} />
        </div>
      )}
    </DashboardLayout>
  );
}

function MetricCard({ title, value, suffix}) {
  return (
    <div className="bg-white rounded-3xl p-8 shadow-md border border-slate-200 hover:shadow-lg transition">
      <p className="text-sm text-slate-500">{title}</p>
      <h2 className="text-4xl font-bold text-indigo-600 mt-3">
        <CountUp end={value} duration={1.5} /> {suffix}
      </h2>
    </div>
  );
}
