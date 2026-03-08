import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

export default function TopicChart({ data = [] }) {
  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{ top: 10, right: 20, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="topicGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#6366F1" stopOpacity={0.9} />
              <stop offset="100%" stopColor="#6366F1" stopOpacity={0.4} />
            </linearGradient>
          </defs>

          <CartesianGrid strokeDasharray="3 3" vertical={false} />

          <XAxis dataKey="date" tick={{ fontSize: 12 }} stroke="#94A3B8" />

          <YAxis tick={{ fontSize: 12 }} stroke="#94A3B8" />

          <Tooltip
            cursor={{ fill: "rgba(99,102,241,0.1)" }}
            contentStyle={{
              borderRadius: "10px",
              border: "none",
              boxShadow: "0 4px 14px rgba(0,0,0,0.1)",
            }}
          />

          <Bar
            dataKey="hours"
            fill="url(#topicGradient)"
            radius={[8, 8, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
