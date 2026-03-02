import { useState, useEffect } from "react";
import { Loader2, ChevronUp, ChevronDown } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import toast from "react-hot-toast";
import API from "../api";
import EntryList from "./EntryList";

export default function EntryForm({ refresh }) {
  const [date, setDate] = useState("");
  const [hours, setHours] = useState("");
  const [topic, setTopic] = useState("");
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    fetchEntries();
  }, []);

  const fetchEntries = async () => {
    try {
      const res = await API.get("/learning/");
      setEntries(Array.isArray(res.data) ? res.data : []);
    } catch {
      toast.error("Failed to load entries");
      setEntries([]);
    }
  };

  const submit = async (e) => {
    e.preventDefault();

    if (!date || !hours || !topic.trim()) {
      toast.error("All fields are required.");
      return;
    }

    if (isNaN(Number(hours))) {
      toast.error("Hours must be a valid number.");
      return;
    }

    const optimisticEntry = {
      id: Date.now(), // temporary ID
      date,
      hours,
      topic,
    };

    setEntries((prev) => [optimisticEntry, ...prev]);

    try {
      setLoading(true);

      const res = await API.post("/learning/", {
        date,
        hours: Number(hours),
        topic: topic.trim(),
      });
      setEntries((prev) =>
        prev.map((e) => (e.id === optimisticEntry.id ? res.data : e)),
      );

      toast.success("Entry added successfully..");

      setDate("");
      setHours("");
      setTopic("");

      setCollapsed(true);

      if (refresh) refresh();
    } catch (err) {
      toast.error(
        err.response?.data?.detail ||
          "Something went wrong while adding entry.",
      );

      // rollback
      fetchEntries();
    } finally {
      setLoading(false);
    }
  };

  const deleteEntry = async (id) => {
    const oldEntries = entries;
    setEntries((prev) => prev.filter((e) => e.id !== id));

    try {
      await API.delete(`/learning/${id}`);
      toast.success("Entry deleted");
      if (refresh) refresh();
    } catch {
      toast.error("Delete failed");
      setEntries(oldEntries);
    }
  };

  const uniqueTopics = [
    ...new Set(entries.map((e) => e.topic).filter(Boolean)),
  ];

  return (
    <div className="space-y-8">
      {/* Collapsible Header */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="flex items-center gap-2 text-indigo-600 font-medium"
      >
        {collapsed ? <ChevronDown size={18} /> : <ChevronUp size={18} />}
        {collapsed ? "Add New Entry" : "Hide Form"}
      </button>

      <AnimatePresence>
        {!collapsed && (
          <motion.form
            onSubmit={submit}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6"
          >
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
              className="px-4 py-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 outline-none"
            />

            <input
              type="number"
              step="0.1"
              placeholder="Hours"
              value={hours}
              onChange={(e) => setHours(e.target.value)}
              required
              className="px-4 py-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 outline-none"
            />

            <input
              list="topics"
              type="text"
              placeholder="Topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              required
              className="px-4 py-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 outline-none"
            />

            <datalist id="topics">
              {uniqueTopics.map((t) => (
                <option key={t} value={t} />
              ))}
            </datalist>

            <button
              type="submit"
              disabled={loading}
              className="md:col-span-3 flex justify-center items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl font-medium disabled:opacity-50"
            >
              {loading && <Loader2 className="animate-spin" size={18} />}
              {loading ? "Adding..." : "Add Entry"}
            </button>
          </motion.form>
        )}
      </AnimatePresence>

      {/* Entry List */}
      <EntryList
        entries={entries}
        onDelete={deleteEntry}
        onEdit={(entry) => {
          setDate(entry.date);
          setHours(entry.hours);
          setTopic(entry.topic);
          setCollapsed(false);
        }}
      />
    </div>
  );
}
