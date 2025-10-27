// frontend/hooks/useWebSocket.ts
import { useEffect, useRef } from "react";

export const useWebSocket = (url: string) => {
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    socketRef.current = new WebSocket(url);

    socketRef.current.onopen = () => console.log("WS connected");
    socketRef.current.onclose = () => console.log("WS disconnected");

    return () => socketRef.current?.close();
  }, [url]);

  const sendMessage = (msg: any) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(msg));
    }
  };

  return { socket: socketRef.current, sendMessage };
};