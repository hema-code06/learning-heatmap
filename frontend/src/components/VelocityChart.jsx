import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

export default function VelocityChart({ data }) {
  
  // Convert backend object → array for recharts
  const chartData = Object.entries(data || {}).map(([date, hours]) => ({
    date: new Date(date).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    }),
    hours,
  }));

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={chartData}
          margin={{ top: 10, right: 20, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="velocityGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366F1" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#6366F1" stopOpacity={0} />
            </linearGradient>
          </defs>

          <CartesianGrid strokeDasharray="3 3" vertical={false} />

          <XAxis
            dataKey="date"
            tick={{ fontSize: 12 }}
            stroke="#94A3B8"
          />

          <YAxis
            tick={{ fontSize: 12 }}
            stroke="#94A3B8"
          />

          <Tooltip
            formatter={(value) => [`${value} hrs`, "Study Time"]}
            contentStyle={{
              borderRadius: "10px",
              border: "none",
              boxShadow: "0 4px 14px rgba(0,0,0,0.1)",
            }}
          />

          <Area
            type="monotone"
            dataKey="hours"
            stroke="#6366F1"
            strokeWidth={3}
            fill="url(#velocityGradient)"
            dot={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}