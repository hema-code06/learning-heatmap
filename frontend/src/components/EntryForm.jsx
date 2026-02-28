import { useState } from "react";
import API from "../api";

export default function EntryForm({ refresh }) {
  const [date, setDate] = useState("");
  const [hours, setHours] = useState("");
  const [topic, setTopic] = useState("");

  const submit = async () => {
    await API.post("/learning", {
      date,
      hours: parseFloat(hours),
      topic,
    });
    refresh();
  };
  return (
    <div>
      <h3>Add Entry</h3>
      <input type="date" onChange={(e) => setDate(e.target.value)} />
      <input type="Hours" onChange={(e) => setHours(e.target.value)} />
      <input type="Topic" onChange={(e) => setTopic(e.target.value)} />
      <button onClick={submit}>Add</button>
    </div>
  );
}
