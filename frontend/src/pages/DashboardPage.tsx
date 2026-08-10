import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { fetchDashboardMetrics } from "../services/dashboard";
import DashboardOverview from "../components/DashboardOverview";
import RecentTickets from "../components/RecentTickets";
import type { DashboardMetrics, Ticket } from "../types";

export default function DashboardPage() {
  const { user } = useAuth();
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardMetrics()
      .then((data) => setMetrics(data))
      .catch((err) => {
        console.error("Error fetching dashboard metrics:", err);
        setMetrics(null);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-8">
      <div className="rounded-[2rem] bg-white p-8 shadow-sm">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Enterprise AI Ticket Resolution System</p>
            <h1 className="mt-3 text-4xl font-semibold text-slate-900">Dashboard</h1>
            <p className="mt-2 text-slate-600">Welcome back, {user?.full_name}.</p>
          </div>
        </div>
      </div>

      <DashboardOverview metrics={metrics} loading={loading} />
      <RecentTickets 
      tickets={(metrics?.recent_tickets as unknown as Ticket[]) || []} 
      loading={loading} />
    </div>
  );
}
