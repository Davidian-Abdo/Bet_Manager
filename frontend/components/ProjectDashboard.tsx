// frontend/components/ProjectDashboard.tsx
import React, { useEffect, useState } from "react";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

// Define the project type
interface Project {
  id: number;
  name: string;
  progress: number;
  budgetUsed: number;
}

// Functional component
const ProjectDashboard: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);

  useEffect(() => {
    // Fetch projects from backend API
    fetch("http://localhost:8000/api/projects")
      .then((res) => {
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
      })
      .then((data: Project[]) => {
        setProjects(data);
        // Adjust Streamlit iframe height dynamically
        Streamlit.setFrameHeight(400 + data.length * 50);
      })
      .catch((error) => {
        console.error("Error fetching projects:", error);
      });
  }, []);

  return (
    <div style={{ padding: "1rem", fontFamily: "Inter, sans-serif" }}>
      <h3>📊 Suivi des Projets</h3>
      {projects.length === 0 ? (
        <p>Aucun projet disponible</p>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={projects}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="progress" fill="#2563eb" name="Avancement (%)" />
            <Bar dataKey="budgetUsed" fill="#10b981" name="Budget utilisé (MAD)" />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
};

// Export with Streamlit connection wrapper
export default withStreamlitConnection(ProjectDashboard);