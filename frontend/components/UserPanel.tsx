import React, { useEffect, useState } from "react";
import axios from "axios";

interface UserPerformance {
  user_name: string;
  avg_task_completion: number;
  on_time_delivery: number;
  quality_score: number;
}

interface UserPanelProps {
  token?: string;
}

const UserPanel: React.FC<UserPanelProps> = ({ token }) => {
  const [users, setUsers] = useState<UserPerformance[]>([]);

  useEffect(() => {
    const fetchPerformance = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/analytics/team", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUsers(res.data);
      } catch (error) {
        console.error("Failed to load team performance:", error);
      }
    };

    fetchPerformance();
  }, [token]);

  return (
    <div className="p-4 bg-white rounded-2xl shadow-md">
      <h3 className="text-lg font-semibold mb-3">Team Performance</h3>
      <ul>
        {users.map((u) => (
          <li key={u.user_name} className="border-b py-2 text-sm">
            <span className="font-medium">{u.user_name}</span> — {u.avg_task_completion}% completion, {u.on_time_delivery}% on time, Quality: {u.quality_score}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserPanel;