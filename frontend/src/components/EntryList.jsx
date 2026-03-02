import { Pencil, Trash2 } from "lucide-react";
import { motion } from "framer-motion";

export default function EntryList({ entries, onDelete, onEdit }) {
  if (!entries.length) return <p className="text-slate-400">No entries yet.</p>;

  return (
    <div className="space-y-3">
      {entries.map((entry) => (
        <motion.div
          key={entry.id}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex justify-between items-center bg-slate-50 border border-slate-200 rounded-xl p-4"
        >
          <div>
            <p className="font-medium text-slate-700">{entry.topic}</p>
            <p className="text-sm text-slate-500">
              {entry.date} • {entry.hours} hrs
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => onEdit(entry)}
              className="text-indigo-500 hover:text-indigo-700"
            >
              <Pencil size={18} />
            </button>

            <button
              onClick={() => onDelete(entry.id)}
              className="text-red-500 hover:text-red-700"
            >
              <Trash2 size={18} />
            </button>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
