import { useState, useEffect } from "react";
import { LayoutDashboard, Plus } from "lucide-react";
import EntryForm from "../components/EntryForm";
import API from "../api";

export default function DashboardLayout({ children }) {
  const [entries, setEntries] = useState([]);
  const [loadingEntries, setLoadingEntries] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editingEntry, setEditingEntry] = useState(null);

  const fetchEntries = async () => {
    try {
      setLoadingEntries(true);
      const res = await API.get("/");
      setEntries(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Fetch entries error:", err);
      setEntries([]);
    } finally {
      setLoadingEntries(false);
    }
  };

  useEffect(() => {
    fetchEntries();
  }, []);

  const handleEdit = (entry) => {
    setEditingEntry(entry);
    setShowModal(true);
  };

  return (
    <div className="flex h-screen bg-slate-100">
      {/* Sidebar */}
      <aside className="w-72 bg-white border-r border-slate-200 shadow-sm p-6 flex flex-col">
        <div className="flex items-center gap-2 mb-8">
          <LayoutDashboard className="text-blue-600" />
          <h2 className="text-2xl font-bold text-blue-600">LearnTrack</h2>
        </div>

        <button
          onClick={() => {
            setEditingEntry(null);
            setShowModal(true);
          }}
          className="mb-6 flex items-center justify-center gap-2 bg-blue-600 text-white py-2 rounded-xl hover:bg-blue-700 transition"
        >
          <Plus size={16} />
          Add Entry
        </button>

        <div className="flex-1 overflow-y-auto">
          <h3 className="text-sm text-slate-500 mb-3">Recent Entries</h3>

          {loadingEntries ? (
            <p className="text-sm text-slate-400">Loading...</p>
          ) : entries.length === 0 ? (
            <p className="text-sm text-slate-400">No entries yet</p>
          ) : (
            <ul className="space-y-2 text-sm">
              {entries.map((entry) => (
                <li
                  key={entry.id}
                  className="p-3 rounded-xl hover:bg-slate-100 cursor-pointer transition"
                  onClick={() => handleEdit(entry)}
                >
                  <div className="flex justify-between">
                    <span className="font-medium text-slate-700">
                      {entry.topic}
                    </span>
                    <span className="text-slate-400">{entry.hours}h</span>
                  </div>

                  <div className="text-xs text-slate-400 mt-1">
                    {new Date(entry.created_at).toLocaleDateString()}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="mt-6 text-xs text-slate-400 text-center">
          Demo Learning Dashboard
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto p-10 relative">
        {children}

        {/* Modal */}
        {showModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
            <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-lg relative">
              <button
                onClick={() => setShowModal(false)}
                className="absolute top-3 right-3 text-slate-500 hover:text-slate-700"
              >
                ✕
              </button>

              <EntryForm
                entries={entries}
                setEntries={setEntries}
                refresh={() => {
                  fetchEntries();
                  setShowModal(false);
                }}
                editingEntry={editingEntry}
                collapsed={false}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
