import { useState, useEffect } from "react";
import { Loader2, ChevronUp, ChevronDown } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import toast from "react-hot-toast";
import API from "../api";
import EntryList from "./EntryList";

export default function EntryForm({ refresh }) {
  // Core
  const [date, setDate] = useState("");
  const [hours, setHours] = useState("");
  const [topic, setTopic] = useState("");
  const [notes, setNotes] = useState("");

  // Purpose of Session
  const [clarityGoal, setClarityGoal] = useState("");
  const [practicalGoal, setPracticalGoal] = useState("");
  const [problemTarget, setProblemTarget] = useState("");
  const [skillFocus, setSkillFocus] = useState("");
  const [successCriteria, setSuccessCriteria] = useState("");

  // Project Section
  const [projectName, setProjectName] = useState("");
  const [projectPurpose, setProjectPurpose] = useState("");
  const [implementationSummary, setImplementationSummary] = useState("");
  const [challenge, setChallenge] = useState("");
  const [solution, setSolution] = useState("");
  const [selfReview, setSelfReview] = useState("");

  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState(null);
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

  const validateFields = () => {
    if (!date || !hours || !topic.trim()) {
      toast.error("All fields are required.");
      return false;
    }

    if (isNaN(Number(hours))) {
      toast.error("Hours must be a valid number.");
      return false;
    }

    const purposeFields = [
      clarityGoal,
      practicalGoal,
      problemTarget,
      skillFocus,
      successCriteria,
    ];

    const projectFields = [
      projectName,
      projectPurpose,
      implementationSummary,
      challenge,
      solution,
      selfReview,
    ];

    if (purposeFields.some((f) => !f.trim())) {
      toast.error("All Purpose of Session fields are required.");
      return false;
    }

    if (projectFields.some((f) => !f.trim())) {
      toast.error("All Project Section fields are required.");
      return false;
    }

    return true;
  };

  const resetForm = () => {
    setDate("");
    setHours("");
    setTopic("");
    setNotes("");

    setClarityGoal("");
    setPracticalGoal("");
    setProblemTarget("");
    setSkillFocus("");
    setSuccessCriteria("");

    setProjectName("");
    setProjectPurpose("");
    setImplementationSummary("");
    setChallenge("");
    setSolution("");
    setSelfReview("");

    setEditingId(null);
  };

  const submit = async (e) => {
    e.preventDefault();

    if (!validateFields()) return;
    const payload = {
      date,
      hours: Number(hours),
      topic: topic.trim(),
      notes,

      purpose: {
        clarity_goal: clarityGoal,
        practical_goal: practicalGoal,
        problem_target: problemTarget,
        skill_focus: skillFocus,
        success_criteria: successCriteria,
      },

      project: {
        project_name: projectName,
        project_purpose: projectPurpose,
        implementation_summary: implementationSummary,
        challenge,
        solution,
        self_review: selfReview,
      },
    };

    try {
      setLoading(true);

      if (editingId) {
        const res = await API.put(`/learning/${editingId}`, payload);

        setEntries((prev) =>
          prev.map((e) => (e.id === editingId ? res.data : e)),
        );

        toast.success("Entry updated successfully.");
        setEditingId(null);
      } else {
        const res = await API.post("/learning/", payload);

        setEntries((prev) => [res.data, ...prev]);
        toast.success("Entry added successfully.");
      }
      resetForm();
      setCollapsed(true);

      if (refresh) refresh();
    } catch (err) {
      console.log("PUT error full:", err.response?.data);
      toast.error(
        err.response?.data?.detail?.[0]?.msg || "Something went wrong.",
      );
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
            className="space-y-10"
          >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
                className="input"
              />
              <input
                type="number"
                step="0.1"
                placeholder="Hours"
                value={hours}
                onChange={(e) => setHours(e.target.value)}
                required
                className="input"
              />
              <input
                list="topics"
                type="text"
                placeholder="Topic"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                required
                className="input"
              />
              <datalist id="topics">
                {uniqueTopics.map((t) => (
                  <option key={t} value={t} />
                ))}
              </datalist>
            </div>

            <textarea
              placeholder="Notes (optional)"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="input w-full"
            />

            {/* Purpose Section */}
            <div>
              <h3 className="font-semibold text-lg mb-4">Purpose of Session</h3>
              <div className="space-y-4">
                <textarea
                  placeholder="Clarity Goal"
                  value={clarityGoal}
                  onChange={(e) => setClarityGoal(e.target.value)}
                  className="input w-full"
                />
                <textarea
                  placeholder="Practical Goal"
                  value={practicalGoal}
                  onChange={(e) => setPracticalGoal(e.target.value)}
                  className="input w-full"
                />
                <textarea
                  placeholder="Problem Target"
                  value={problemTarget}
                  onChange={(e) => setProblemTarget(e.target.value)}
                  className="input w-full"
                />
                <textarea
                  placeholder="Skill Focus"
                  value={skillFocus}
                  onChange={(e) => setSkillFocus(e.target.value)}
                  className="input w-full"
                />
                <textarea
                  placeholder="Success Criteria"
                  value={successCriteria}
                  onChange={(e) => setSuccessCriteria(e.target.value)}
                  className="input w-full"
                />
              </div>
            </div>

            {/* Project Section */}
            <div>
              <h3 className="font-semibold text-lg mb-4">Project Section</h3>
              <div className="space-y-4">
                <input
                  placeholder="Project Name"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                  className="input w-full"
                />
                <textarea
                  placeholder="Project Purpose"
                  value={projectPurpose}
                  onChange={(e) => setProjectPurpose(e.target.value)}
                  className="input w-full"
                />
                <textarea
                  placeholder="Implementation Summary"
                  value={implementationSummary}
                  onChange={(e) => setImplementationSummary(e.target.value)}
                  className="input w-full"
                />
                <textarea
                  placeholder="Biggest Challenge"
                  value={challenge}
                  onChange={(e) => setChallenge(e.target.value)}
                  className="input w-full"
                />
                <textarea
                  placeholder="Solution Applied"
                  value={solution}
                  onChange={(e) => setSolution(e.target.value)}
                  className="input w-full"
                />
                <textarea
                  placeholder="Self Review / What to Improve"
                  value={selfReview}
                  onChange={(e) => setSelfReview(e.target.value)}
                  className="input w-full"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 text-white py-3 rounded-xl font-medium disabled:opacity-50 flex justify-center items-center gap-2"
            >
              {loading && <Loader2 className="animate-spin" size={18} />}
              {loading ? "Adding..." : "Add Entry"}
            </button>
          </motion.form>
        )}
      </AnimatePresence>

      <EntryList
        entries={entries}
        onDelete={deleteEntry}
        onEdit={(entry) => {
          setDate(entry.date.split("T")[0]);
          setHours(String(entry.hours));
          setTopic(entry.topic);
          setEditingId(entry.id);
          setCollapsed(false);
        }}
      />
    </div>
  );
}
