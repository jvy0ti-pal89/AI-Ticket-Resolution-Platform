import { Link } from "react-router-dom";
import type { Ticket } from "../types";

interface RecentTicketsProps {
  tickets: Ticket[];
  loading: boolean;
}

export default function RecentTickets({ tickets, loading }: RecentTicketsProps) {
  const recent = tickets.slice(0, 5);

  return (
    <div className="rounded-[2rem] bg-white p-8 shadow-sm">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">Recent Tickets</h2>
          <p className="text-slate-500">Quick access to your most recent ticket activity.</p>
        </div>
        <Link to="/app/tickets" className="text-sm font-medium text-indigo-600 hover:text-indigo-700">
          View all
        </Link>
      </div>

      <div className="space-y-3">
        {loading ? (
          <p className="text-slate-500">Loading tickets...</p>
        ) : recent.length === 0 ? (
          <p className="text-slate-500">No recent tickets yet.</p>
        ) : (
          <div className="overflow-hidden rounded-3xl border border-slate-200">
            <div className="grid grid-cols-4 gap-4 bg-slate-100 px-6 py-4 text-sm uppercase tracking-[0.18em] text-slate-500">
              <div>Title</div>
              <div>Category</div>
              <div>Priority</div>
              <div>Status</div>
            </div>
            {recent.map((ticket) => (
              <Link
                key={ticket.id}
                to={`/app/tickets/${ticket.id}`}
                className="grid grid-cols-4 gap-4 border-t border-slate-200 px-6 py-4 transition hover:bg-slate-50"
              >
                <div className="font-medium text-slate-900">{ticket.title}</div>
                <div className="text-slate-600">{ticket.category || "General"}</div>
                <div className="text-slate-600">{ticket.priority || "Medium"}</div>
                <div className="text-slate-600">{ticket.status}</div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
