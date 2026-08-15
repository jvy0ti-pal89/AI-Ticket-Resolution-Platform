import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Automatically attach stored JWT token to every outgoing request.

api.interceptors.request.use((config) => {
  // Check for 'ai_ticket_token', fallback to 'token' or 'access_token'
  const token =
    localStorage.getItem("ai_ticket_token") ||
    localStorage.getItem("token") ||
    localStorage.getItem("access_token");

  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export const setAuthToken = (token: string | null) => {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common.Authorization;
  }
};

export default api;
