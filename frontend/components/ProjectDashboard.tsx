import React, { useEffect, useState } from "react";
import axios from "axios";

interface KPIData {
  project_name: string;
  average_progress: number;
  budget_total: number;
  budget_spent: number;
  current_margin: number;
}

interface ProjectDashboardProps {
  projectId: number;
  token?: string;
  backendUrl: string; // <- added backend URL prop
}

const ProjectDashboard: React.FC<ProjectDashboardProps> = ({ projectId, token, backendUrl }) => {
  const [kpis, setKpis] = useState<KPIData | null>(null);

  useEffect(() => {
    const fetchKpis = async () => {
      try {
        const res = await axios.get(`${backendUrl}/analytics/project/${projectId}`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        });
        setKpis(res.data);
      } catch (error) {
        console.error("Failed to fetch KPIs:", error);
      }
    };

    fetchKpis();
  }, [projectId, token, backendUrl]); // include backendUrl as dependency

  if (!kpis) return <p>Loading project KPIs...</p>;

  return (
    <div className="grid grid-cols-2 gap-4 p-4 bg-white shadow-md rounded-2xl">
      <h2 className="col-span-2 text-xl font-semibold">{kpis.project_name}</h2>
      <p>Average Progress: {kpis.average_progress.toFixed(1)}%</p>
      <p>Budget Total: ${kpis.budget_total.toLocaleString()}</p>
      <p>Budget Spent: ${kpis.budget_spent.toLocaleString()}</p>
      <p>Margin: {kpis.current_margin}%</p>
    </div>
  );
};

export default ProjectDashboard
