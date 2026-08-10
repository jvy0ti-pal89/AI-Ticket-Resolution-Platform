import api from "./api";
import type { User } from "../types";

export async function fetchUsers() {
  const response = await api.get<User[]>("/users");
  return response.data;
}

export async function deleteUser(id: string) {
  const response = await api.delete(`/users/${id}`);
  return response.data;
}