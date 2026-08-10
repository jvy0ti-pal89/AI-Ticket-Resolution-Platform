import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { fetchTicket, reviewTicket, updateTicket } from "../services/tickets";
import type { Ticket } from "../types";

export default function TicketDetailPage() {
  const { ticketId } = useParams();
  const navigate = useNavigate();
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState(false);
  const [editResolution, setEditResolution] = useState("");
  const [isReviewing, setIsReviewing] = useState(false);

  useEffect(() => {
    if (!ticketId) return;
    fetchTicket(Number(ticketId))
      .then((data) => {
        setTicket(data);
        setStatus(data.status);
      })
      .catch(() => setError("Unable to load ticket."))
      .finally(() => setLoading(false));
  }, [ticketId]);

  const handleSave = async () => {
    if (!ticket?.id) return;
    try {
      const updated = await updateTicket(ticket.id, { status });
      setTicket(updated);
      navigate("/app/tickets");
    } catch (err) {
      setError("Unable to update ticket.");
    }
  };

  const handleReview = async (action: "approve" | "edit" | "escalate") => {
    if (!ticket?.id) return;
    setError(null);
    setIsReviewing(true);

    try {
      const payload: {
        action: "approve" | "edit" | "escalate";
        resolution?: string;
        escalation_reason?: string;
      } = { action };

      if (action === "edit") {
        payload.resolution = editResolution;
      }

      const updated = await reviewTicket(ticket.id, payload);
      setTicket(updated);
      setStatus(updated.status);
      setEditing(false);
    } catch (err) {
      setError("Unable to complete review action.");
    } finally {
      setIsReviewing(false);
    }
  };

  const beginEdit = () => {
    setEditResolution(ticket?.resolution || "");
    setEditing(true);
  };

  const cancelEdit = () => {
    setEditing(false);
    setEditResolution("");
  };

  if (loading) {
    return <div className="min-h-screen bg-slate-50 p-6">Loading...</div>;
  }

  if (!ticket) {
    return <div className="min-h-screen bg-slate-50 p-6">Ticket not found.</div>;
  }

  const isPendingReview = ticket.status === "PENDING_REVIEW";
  const isResolved = ticket.status === "RESOLVED";
  const isEscalated = ticket.status === "ESCALATED";

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="rounded-2xl bg-white p-6 shadow-sm">
        <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold">{ticket.title}</h1>
            <p className="text-slate-500">
              {ticket.category || "General"} • {ticket.priority || "Medium"} • {ticket.status}
            </p>
          </div>
          <button
            onClick={() => navigate(-1)}
            className="rounded-md border border-slate-300 px-4 py-2 hover:bg-slate-100"
          >
            Back
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <h2 className="text-lg font-semibold">Description</h2>
            <p className="mt-2 text-slate-600">{ticket.description}</p>
          </div>

          <div>
            <h2 className="text-lg font-semibold">Summary</h2>
            <p className="mt-2 text-slate-600">{ticket.summary || "No summary available."}</p>
          </div>

          <div>
            <h2 className="text-lg font-semibold">
              {isPendingReview ? "AI Suggested Resolution" : "Final Resolution"}
            </h2>
            {editing ? (
              <textarea
                value={editResolution}
                onChange={(e) => setEditResolution(e.target.value)}
                rows={6}
                className="mt-2 w-full rounded-md border border-slate-300 px-3 py-2"
              />
            ) : (
              <p className="mt-2 text-slate-600">
                {ticket.resolution || "No resolution available yet."}
              </p>
            )}
          </div>

          {ticket.reviewed_at && (
            <div>
              <p className="text-sm text-slate-500">
                Reviewed at {new Date(ticket.reviewed_at).toLocaleString()}
              </p>
            </div>
          )}

          {ticket.escalation_reason && (
            <div>
              <h2 className="text-lg font-semibold">Escalation Reason</h2>
              <p className="mt-2 text-slate-600">{ticket.escalation_reason}</p>
            </div>
          )}

          {error && <p className="text-sm text-red-600">{error}</p>}

          {isPendingReview && !editing && (
            <div className="flex flex-col gap-3 md:flex-row">
              <button
                onClick={() => handleReview("approve")}
                disabled={isReviewing}
                className="rounded-md bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-700"
              >
                Approve
              </button>
              <button
                onClick={beginEdit}
                disabled={isReviewing}
                className="rounded-md bg-slate-100 px-4 py-2 text-slate-700 hover:bg-slate-200"
              >
                Edit
              </button>
              <button
                onClick={() => handleReview("escalate")}
                disabled={isReviewing}
                className="rounded-md bg-amber-500 px-4 py-2 text-white hover:bg-amber-600"
              >
                Escalate
              </button>
            </div>
          )}

          {editing && (
            <div className="flex flex-col gap-3 md:flex-row">
              <button
                onClick={() => handleReview("edit")}
                disabled={isReviewing || !editResolution.trim()}
                className="rounded-md bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700"
              >
                Save Resolution
              </button>
              <button
                onClick={cancelEdit}
                disabled={isReviewing}
                className="rounded-md bg-slate-100 px-4 py-2 text-slate-700 hover:bg-slate-200"
              >
                Cancel
              </button>
            </div>
          )}

          <div>
            <h2 className="text-lg font-semibold">Status</h2>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="mt-2 w-full rounded-md border border-slate-300 px-3 py-2"
            >
              <option value="OPEN">OPEN</option>
              <option value="PENDING_REVIEW">PENDING_REVIEW</option>
              <option value="RESOLVED">RESOLVED</option>
              <option value="ESCALATED">ESCALATED</option>
            </select>
          </div>

          <button
            onClick={handleSave}
            className="rounded-md bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700"
          >
            Save Status
          </button>
        </div>
      </div>
    </div>
  );
}
