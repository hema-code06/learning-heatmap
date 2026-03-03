import { useEffect, useState } from "react";
import API from "../api";
import Card from "./ui/Card";

export default function BadgePanel() {
  const [badges, setBadges] = useState([]);

  useEffect(() => {
    const fetchBadges = async () => {
      const res = await API.get("/learning/badges");
      setBadges(res.data);
    };
    fetchBadges();
  }, []);

  return (
    <Card>
      <h2 className="text-lg font-semibold mb-4">Achievements</h2>
      {badges.length === 0 ? (
        <p className="text-slate-400">No badges yet</p>
      ) : (
        <ul className="space-y-2">
          {badges.map((badge) => (
            <li key={badge.name} className="bg-slate-100 p-2 rounded-lg">
              {badge.name}
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}