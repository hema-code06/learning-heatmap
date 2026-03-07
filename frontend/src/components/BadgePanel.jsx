import { useEffect, useState } from "react";
import API from "../api";
import Card from "./ui/Card";
import { Trophy, Flame, Star } from "lucide-react";

export default function BadgePanel() {
  const [badges, setBadges] = useState([]);

  useEffect(() => {
    const fetchBadges = async () => {
      try {
        const res = await API.get("/learning/badges");
        setBadges(res.data);
      } catch (err) {
        console.error("Failed to load badges", err);
      }
    };

    fetchBadges();
  }, []);

  const badgeIcon = (name) => {
    if (name.toLowerCase().includes("streak"))
      return <Flame className="text-orange-500" size={20} />;
    if (name.toLowerCase().includes("goal"))
      return <Star className="text-indigo-500" size={20} />;
    return <Trophy className="text-yellow-500" size={20} />;
  };

  return (
    <Card title="Achievements">

      {badges.length === 0 ? (
        <div className="text-slate-400 text-sm">
          No achievements yet. Keep learning!
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">

          {badges.map((badge) => (
            <div
              key={badge.name}
              className="flex items-center gap-2 bg-slate-50 border rounded-xl p-3 hover:shadow-sm transition"
            >
              {badgeIcon(badge.name)}

              <span className="text-sm font-medium text-slate-700">
                {badge.name}
              </span>

            </div>
          ))}

        </div>
      )}

    </Card>
  );
}