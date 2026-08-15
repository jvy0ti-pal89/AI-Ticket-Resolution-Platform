import { createContext, useContext, useEffect, useMemo, useState } from "react";
import api, { setAuthToken } from "../services/api";
import type { User } from "../types";

interface AuthContextValue {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);
const storageTokenKey = "ai_ticket_token";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => 
    localStorage.getItem(storageTokenKey)
  );
  const [loading, setLoading] = useState(true);

  const fetchCurrentUser = async (authToken: string) => {
    try {
      setAuthToken(authToken);
      const response = await api.get<User>("/auth/me");
      setUser(response.data);
      setToken(authToken);
    } catch (err: any) {
      console.error("Failed to fetch user profile:", err);
      if (err.response?.status === 401) {
        logout();
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const savedToken = localStorage.getItem(storageTokenKey);
    if (savedToken) {
      fetchCurrentUser(savedToken);
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    const response = await api.post("/auth/login", { email, password });
    const authToken = response.data.access_token || response.data.token;

    // Immediately save and set headers before calling /auth/me
    localStorage.setItem(storageTokenKey, authToken);
    setAuthToken(authToken);
    setToken(authToken);

    // Fetch user details immediately to verify role string
    const userResponse = await api.get<User>("/auth/me");
    setUser(userResponse.data);
    setLoading(false);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem(storageTokenKey);
    setAuthToken(null);
  };

  const value = useMemo(
    () => ({ user, token, loading, login, logout }),
    [user, token, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}