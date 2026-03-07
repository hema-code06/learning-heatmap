import Card from "./ui/Card";
import { RadialBarChart, RadialBar, ResponsiveContainer } from "recharts";

export default function ProductivityCard({ data }) {
  if (!data) return null;

  const chartData = [
    {
      name: "score",
      value: data.productivity_score,
      fill: "#6366F1",
    },
  ];

  return (
    <Card title="Average Performance">
      <div className="flex flex-col items-center justify-center">
        <div className="w-full h-64">
          <ResponsiveContainer>
            <RadialBarChart
              innerRadius="70%"
              outerRadius="100%"
              data={chartData}
              startAngle={90}
              endAngle={-270}
            >
              <RadialBar minAngle={15} background clockWise dataKey="value" />
            </RadialBarChart>
          </ResponsiveContainer>
        </div>

        <div className="text-center -mt-20">
          <h2 className="text-4xl font-bold text-indigo-600">
            {data.productivity_score}
          </h2>

          <p className="text-slate-500 text-sm mt-1">{data.label}</p>
        </div>
      </div>
    </Card>
  );
}
