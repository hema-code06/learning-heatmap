import Heatmap from "../components/Heatmap";
import EntryForm from "../components/EntryForm";

export default function Dashboard() {
  const refresh = () => window.location.reload();

  return (
    <div>
      <h1>Dashboard</h1>
      <EntryForm refresh={refresh} />
      <Heatmap />
    </div>
  );
}
