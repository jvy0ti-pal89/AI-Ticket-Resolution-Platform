import { Link } from "react-router-dom";
import type { DashboardMetrics } from "../types";

interface DashboardOverviewProps {
  metrics: DashboardMetrics | null;
  loading: boolean;
}

export default function DashboardOverview({
  metrics,
  loading,
}: DashboardOverviewProps) {
  const cards = [
    { label: "Total Tickets", value: metrics?.total_tickets ?? 0 },
    { label: "Open Tickets", value: metrics?.open_tickets ?? 0 },
    { label: "Pending Review", value: metrics?.pending_review ?? 0 },
    { label: "Resolved Tickets", value: metrics?.resolved_tickets ?? 0 },
    { label: "Escalated Tickets", value: metrics?.escalated_tickets ?? 0 },
    { label: "High Priority", value: metrics?.high_priority_tickets ?? 0 },
  ];

  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] bg-white p-8 shadow-sm">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm text-slate-600">
              Overview of ticket health and recent activity.
            </p>
          </div>

          <Link
            to="/app/tickets"
            className="inline-flex items-center justify-center rounded-2xl bg-indigo-600 px-6 py-3 text-white shadow-sm hover:bg-indigo-700"
          >
            View all tickets
          </Link>
        </div>

        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {cards.map((card) => (
            <div
              key={card.label}
              className="rounded-3xl border border-slate-200 p-6"
            >
              <p className="text-sm uppercase tracking-[0.2em] text-slate-500">
                {card.label}
              </p>

              <p className="mt-4 text-4xl font-semibold text-slate-900">
                {loading ? "—" : card.value}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-10 grid gap-4 xl:grid-cols-2">
          {/* Category Breakdown */}
          <div className="rounded-3xl border border-slate-200 p-6">
            <h2 className="text-lg font-semibold text-slate-900">
              Category Breakdown
            </h2>

            <div className="mt-4 space-y-3">
              {loading ? (
                <p className="text-slate-500">
                  Loading category breakdown...
                </p>
              ) : metrics?.category_breakdown?.length ? (
                metrics.category_breakdown.map((row) => (
                  <div
                    key={row.category}
                    className="flex items-center justify-between gap-4 rounded-2xl bg-slate-50 px-4 py-3"
                  >
                    <span className="text-slate-700">
                      {row.category}
                    </span>

                    <span className="font-semibold text-slate-900">
                      {row.count}
                    </span>
                  </div>
                ))
              ) : (
                <p className="text-slate-500">
                  No category data available.
                </p>
              )}
            </div>
          </div>

          {/* High Priority Tickets */}
          <div className="rounded-3xl border border-slate-200 p-6">
            <h2 className="text-lg font-semibold text-slate-900">
              High Priority Tickets
            </h2>

            <div className="mt-4 space-y-3">
              {loading ? (
                <p className="text-slate-500">
                  Loading high-priority tickets...
                </p>
              ) : metrics?.high_priority_ticket_list?.length ? (
                metrics.high_priority_ticket_list.map((ticket) => (
                  <Link
                    key={ticket.id}
                    to={`/app/tickets/${ticket.id}`}
                    className="block rounded-2xl bg-slate-50 px-4 py-3 transition hover:bg-slate-100"
                  >
                    <div className="text-sm font-semibold text-slate-900">
                      {ticket.title}
                    </div>

                    <div className="text-xs text-slate-500">
                      {ticket.category || "General"} • {ticket.status}
                    </div>
                  </Link>
                ))
              ) : (
                <p className="text-slate-500">
                  No high-priority tickets.
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}