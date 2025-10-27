// frontend/hooks/useAuth.ts
import { useState } from "react";

export const useAuth = () => {
  const [user, setUser] = useState<any>(null);

  const login = (token: string, userData: any) => {
    localStorage.setItem("access_token", token);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
  };

  return { user, login, logout };
};