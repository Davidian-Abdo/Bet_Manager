// frontend/hooks/useAPI.ts
import axios from "axios";

const API_BASE = "http://localhost:8000/api";

export const useAPI = () => {
  const get = async (endpoint: string) => {
    const token = localStorage.getItem("access_token");
    return await axios.get(`${API_BASE}${endpoint}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
  };

  const post = async (endpoint: string, data: any) => {
    const token = localStorage.getItem("access_token");
    return await axios.post(`${API_BASE}${endpoint}`, data, {
      headers: { Authorization: `Bearer ${token}` }
    });
  };

  return { get, post };
}