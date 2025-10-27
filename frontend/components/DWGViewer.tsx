// frontend/components/DWGViewer.tsx
import React, { useEffect, useRef, useState } from "react";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";
import { useWebSocket } from "../hooks/useWebSocket";

interface DWGViewerProps {
  projectId: number;
  userId: number;
}

const DWGViewer = ({ projectId, userId }: DWGViewerProps) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const { socket, sendMessage } = useWebSocket(`ws://localhost:8000/ws/dwg/${projectId}`);
  const [cursor, setCursor] = useState<{ x: number; y: number }>({ x: 0, y: 0 });

  useEffect(() => {
    if (!canvasRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    if (ctx) ctx.clearRect(0, 0, canvas.width, canvas.height);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "draw") {
        const { x, y } = data.payload;
        ctx?.fillRect(x, y, 2, 2);
      }
    };
  }, [socket]);

  const handleMouseMove = (e: React.MouseEvent) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setCursor({ x, y });
    sendMessage({ type: "cursor", payload: { x, y, userId } });
  };

  return (
    <div>
      <h4>🧰 Collaboration DWG - Projet #{projectId}</h4>
      <canvas
        ref={canvasRef}
        width={800}
        height={600}
        style={{ border: "1px solid #ccc", cursor: "crosshair" }}
        onMouseMove={handleMouseMove}
      />
      <p style={{ color: "gray" }}>Position: {cursor.x}, {cursor.y}</p>
    </div>
  );
};

export default withStreamlitConnection(DWGViewer)