import React from "react";

interface UserPerformance {
  user_name: string;
  avg_task_completion: number;
  on_time_delivery: number;
  quality_score: number;
}

interface UserPanelProps {
  data: UserPerformance[]; // Receive team performance from Streamlit
}

const UserPanel: React.FC<UserPanelProps> = ({ data }) => {
  return (
    <div className="p-4 bg-white rounded-2xl shadow-md">
      <h3 className="text-lg font-semibold mb-3">Team Performance</h3>
      <ul>
        {data.map((u) => (
          <li key={u.user_name} className="border-b py-2 text-sm">
            <span className="font-medium">{u.user_name}</span> — {u.avg_task_completion}% completion, {u.on_time_delivery}% on time, Quality: {u.quality_score}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserPanel;
