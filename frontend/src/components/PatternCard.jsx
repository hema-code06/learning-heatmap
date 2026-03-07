import Card from "./ui/Card";

export default function PatternCard({ pattern }) {
  if (!pattern) return null;

  return (
    <Card title="Weekly Learning Pattern">
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <span className="text-slate-500 text-sm">Dominant Day</span>
          <span className="font-semibold text-indigo-600">
            {pattern.dominant_day}
          </span>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-slate-500 text-sm">Learning Type</span>
          <span className="px-3 py-1 rounded-full text-xs bg-indigo-100 text-indigo-700 font-medium">
            {pattern.learning_type}
          </span>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-slate-500 text-sm">Consistency</span>
          <span className="px-3 py-1 rounded-full text-xs bg-emerald-100 text-emerald-700 font-medium">
            {pattern.consistency_type}
          </span>
        </div>
      </div>
    </Card>
  );
}
