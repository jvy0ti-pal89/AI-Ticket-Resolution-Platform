import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchTickets } from "../services/tickets";
import type { Ticket } from "../types";

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTickets()
      .then((data) => setTickets(data))
      .catch((err) => {
        console.error("Failed to fetch tickets:", err);
        setTickets([]);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Tickets</h1>
          <p className="text-slate-500">View tickets assigned to your role.</p>
        </div>
      </div>

      <div className="space-y-4">
        {loading ? (
          <p className="text-slate-500">Loading tickets...</p>
        ) : tickets.length === 0 ? (
          <p className="text-slate-500">No tickets found.</p>
        ) : (
          tickets.map((ticket) => (
            <Link
              key={ticket.id}
              to={`/app/tickets/${ticket.id}`}
              className="block rounded-2xl bg-white p-5 shadow-sm hover:border-indigo-500 hover:ring-1 hover:ring-indigo-100"
            >
              <div className="flex items-center justify-between gap-4">
                <div>
                  <h2 className="text-lg font-semibold">{ticket.title}</h2>
                  <p className="mt-1 text-sm text-slate-500">{ticket.summary || ticket.description}</p>
                </div>
                <div className="text-right text-sm text-slate-500">
                  <p>{ticket.category || "General"}</p>
                  <p>{ticket.priority || "Medium"}</p>
                </div>
              </div>
            </Link>
          ))
        )}
      </div>
    </div>
  );
}