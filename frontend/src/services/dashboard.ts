import api from "./api";
import type { DashboardMetrics } from "../types";

export async function fetchDashboardMetrics() {
  const response = await api.get<DashboardMetrics>("/dashboard/metrics");
  return response.data;
}
