import { useEffect, useState } from "react";
import { getDashboard, getStudyTime } from "../api";
import DashboardLayout from "../layout/DashboardLayout";
import Card from "../components/ui/Card";
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
  const [velocity, setVelocity] = useState(0);
  const [consistency, setConsistency] = useState(0);
  const [refreshKey, setRefreshKey] = useState(0);
  const [trendData, setTrendData] = useState([]);
  const [topicData, setTopicData] = useState([]);
  const [advanced, setAdvanced] = useState(null);

  const [dailyStreak, setDailyStreak] = useState({
    current_streak: 0,
    longest_streak: 0,
  });

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const dashboardRes = await getDashboard();

        const data = dashboardRes.data.data;

        setVelocity(data.velocity);
        setConsistency(data.consistency);
        setTrendData(data.study_time.daily || []);
        setTopicData(data.topic_breakdown || []);
        setAdvanced({
          pattern: data.pattern,
          insights: data.insights,
          badges: data.badges,
          total_hours: data.total_hours,
        });

        setDailyStreak({
          current_streak: data.daily_streak,
          longest_streak: data.longest_streak,
        });
      } catch (err) {
        console.error("Analytics error:", err);
      }
    };

    fetchAnalytics();
  }, []);

  return (
    <DashboardLayout>
      {/* ===== TOP METRICS ===== */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        <MetricCard
          title="Current Streak"
          value={dailyStreak.current_streak}
          suffix="days"
        />

        <MetricCard
          title="Longest Streak"
          value={dailyStreak.longest_streak}
          suffix="days"
        />

        <MetricCard
          title="Learning Velocity"
          value={velocity}
          suffix="hrs/week"
        />

        <MetricCard title="Consistency Score" value={consistency} suffix="%" />
      </div>

      {/* ===== OVERVIEW SECTION ===== */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8 mb-10">
        {/* Learning Trend */}
        <div className="xl:col-span-2">
          <Card title="Learning Overview">
            {trendData.length === 0 ? (
              <Skeleton height="h-64" />
            ) : (
              <VelocityChart data={trendData} />
            )}
          </Card>
        </div>

        {/* Topic Breakdown */}
        <Card title="Topic Breakdown">
          {topicData.length === 0 ? (
            <Skeleton height="h-64" />
          ) : (
            <TopicChart data={topicData} />
          )}
        </Card>
      </div>

      {/* ===== GOAL SECTION ===== */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-10">
        <Card title="Monthly Learning Goal">
          <GoalTracker />
        </Card>
      </div>

      {/* ===== PRODUCTIVITY ANALYTICS ===== */}
      {advanced && (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-10">
          <ProductivityCard data={advanced} />
          <PatternCard pattern={advanced.pattern} />
        </div>
      )}

      {/* ===== INSIGHTS & BADGES ===== */}
      {advanced && (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-10">
          <InsightsPanel insights={advanced.insights} />
          <BadgePanel badges={advanced.badges} />
        </div>
      )}
    </DashboardLayout>
  );
}

function MetricCard({ title, value, suffix }) {
  return (
    <div className="bg-white rounded-3xl p-6 shadow-md border border-slate-200 hover:shadow-lg transition">
      <p className="text-sm text-slate-500">{title}</p>

      <h2 className="text-3xl font-bold text-indigo-600 mt-3">
        <CountUp end={value || 0} duration={1.5} />
        {suffix && (
          <span className="text-lg text-slate-500 ml-1">{suffix}</span>
        )}
      </h2>
    </div>
  );
}
