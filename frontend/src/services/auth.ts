import api from "./api";
import type { User } from "../types";

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  full_name: string;
  password: string;
  role?: "admin" | "engineer" | "employee";
}

export async function login(payload: LoginPayload) {
  const response = await api.post("/auth/login", payload);
  return response.data;
}

export async function register(payload: RegisterPayload) {
  // Fixed: Points to /auth/register
  const response = await api.post<User>("/auth/register", payload);
  return response.data;
}

export async function getCurrentUser() {
  const response = await api.get<User>("/auth/me");
  return response.data;
}