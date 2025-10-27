// frontend/components/UserPanel.tsx
import React, { useEffect, useState } from "react";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";

interface User {
  name: string;
  role: string;
  active: boolean;
}

const UserPanel = () => {
  const [team, setTeam] = useState<User[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/team/availability")
      .then((res) => res.json())
      .then((data) => {
        setTeam(data);
        Streamlit.setFrameHeight(300);
      });
  }, []);

  return (
    <div style={{ padding: "1rem" }}>
      <h3>👥 Équipe Active</h3>
      {team.map((u) => (
        <div
          key={u.name}
          style={{
            padding: "0.5rem",
            backgroundColor: u.active ? "#dcfce7" : "#fee2e2",
            borderRadius: "8px",
            marginBottom: "4px",
          }}
        >
          <strong>{u.name}</strong> — {u.role}
        </div>
      ))}
    </div>
  );
};

export default withStreamlitConnection(UserPanel);