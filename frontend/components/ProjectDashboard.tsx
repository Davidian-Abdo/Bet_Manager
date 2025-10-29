import React from "react";

interface KPIData {
  project_name: string;
  average_progress: number;
  budget_total: number;
  budget_spent: number;
  current_margin: number;
}

interface ProjectDashboardProps {
  data: KPIData | null; // Receive KPIs from Streamlit
}

const ProjectDashboard: React.FC<ProjectDashboardProps> = ({ data }) => {
  if (!data) return <p>Loading project KPIs...</p>;

  return (
    <div className="grid grid-cols-2 gap-4 p-4 bg-white shadow-md rounded-2xl">
      <h2 className="col-span-2 text-xl font-semibold">{data.project_name}</h2>
      <p>Average Progress: {data.average_progress.toFixed(1)}%</p>
      <p>Budget Total: ${data.budget_total.toLocaleString()}</p>
      <p>Budget Spent: ${data.budget_spent.toLocaleString()}</p>
      <p>Margin: {data.current_margin}%</p>
    </div>
  );
};

export default ProjectDashboard;
