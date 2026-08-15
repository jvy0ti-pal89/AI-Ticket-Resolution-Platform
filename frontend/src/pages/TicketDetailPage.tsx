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
  
  // Edit & Escalation States
  const [editing, setEditing] = useState(false);
  const [editResolution, setEditResolution] = useState("");
  const [escalating, setEscalating] = useState(false);
  const [escalationReason, setEscalationReason] = useState("");
  
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

  const handleSaveStatus = async () => {
    if (!ticket?.id) return;
    try {
      const updated = await updateTicket(ticket.id, { status });
      setTicket(updated);
      navigate("/app/tickets");
    } catch (err) {
      setError("Unable to update ticket status.");
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
        if (!editResolution.trim()) {
          setError("Resolution text cannot be empty.");
          setIsReviewing(false);
          return;
        }
        payload.resolution = editResolution.trim();
      }

      if (action === "escalate") {
        if (!escalationReason.trim()) {
          setError("Please provide a reason for escalation.");
          setIsReviewing(false);
          return;
        }
        payload.escalation_reason = escalationReason.trim();
      }

      const updated = await reviewTicket(ticket.id, payload);
      setTicket(updated);
      setStatus(updated.status);
      setEditing(false);
      setEscalating(false);
    } catch (err: any) {
      console.error("Review action error:", err?.response?.data || err);
      setError(
        err?.response?.data?.detail || "Unable to complete review action."
      );
    } finally {
      setIsReviewing(false);
    }
  };

  const beginEdit = () => {
    setEditResolution(ticket?.resolution || "");
    setEditing(true);
    setEscalating(false);
  };

  const cancelEdit = () => {
    setEditing(false);
    setEditResolution("");
  };

  const beginEscalate = () => {
    setEscalating(true);
    setEditing(false);
  };

  const cancelEscalate = () => {
    setEscalating(false);
    setEscalationReason("");
  };

  if (loading) {
    return <div className="min-h-screen bg-slate-50 p-6">Loading ticket...</div>;
  }

  if (!ticket) {
    return <div className="min-h-screen bg-slate-50 p-6">Ticket not found.</div>;
  }

  const isPendingReview = ticket.status === "PENDING_REVIEW";

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="rounded-2xl bg-white p-6 shadow-sm">
        {/* Header */}
        <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold">{ticket.title}</h1>
            <p className="mt-1 text-slate-500">
              {ticket.category || "General"} • {ticket.priority || "Medium"} •{" "}
              <span className="font-semibold text-slate-700">{ticket.status}</span>
            </p>
          </div>
          <button
            onClick={() => navigate(-1)}
            className="rounded-md border border-slate-300 px-4 py-2 hover:bg-slate-100"
          >
            Back
          </button>
        </div>

        <div className="space-y-6">
          {/* Description */}
          <div>
            <h2 className="text-lg font-semibold">Description</h2>
            <p className="mt-2 text-slate-600">{ticket.description}</p>
          </div>

          {/* Summary */}
          <div>
            <h2 className="text-lg font-semibold">Summary</h2>
            <p className="mt-2 text-slate-600">{ticket.summary || "No summary available."}</p>
          </div>

          {/* Resolution Block */}
          <div>
            <h2 className="text-lg font-semibold">
              {isPendingReview ? "AI Suggested Resolution" : "Final Resolution"}
            </h2>
            {editing ? (
              <textarea
                value={editResolution}
                onChange={(e) => setEditResolution(e.target.value)}
                rows={6}
                className="mt-2 w-full rounded-md border border-slate-300 p-3 focus:outline-indigo-500"
                placeholder="Enter updated resolution..."
              />
            ) : (
              <p className="mt-2 text-slate-600">
                {ticket.resolution || "No resolution available yet."}
              </p>
            )}
          </div>

          {/* Escalation Reason Input Field */}
          {escalating && (
            <div>
              <h2 className="text-lg font-semibold text-amber-700">Reason for Escalation</h2>
              <textarea
                value={escalationReason}
                onChange={(e) => setEscalationReason(e.target.value)}
                rows={3}
                className="mt-2 w-full rounded-md border border-amber-300 p-3 focus:outline-amber-500"
                placeholder="Explain why this ticket is being escalated to human engineers..."
              />
            </div>
          )}

          {/* Display Existing Escalation Reason */}
          {ticket.escalation_reason && !escalating && (
            <div className="rounded-lg bg-amber-50 p-4 border border-amber-200">
              <h2 className="text-sm font-semibold text-amber-800">Escalation Reason</h2>
              <p className="mt-1 text-sm text-amber-700">{ticket.escalation_reason}</p>
            </div>
          )}

          {/* Timestamps */}
          {ticket.reviewed_at && (
            <div>
              <p className="text-sm text-slate-400">
                Reviewed at: {new Date(ticket.reviewed_at).toLocaleString()}
              </p>
            </div>
          )}

          {/* Errors */}
          {error && <p className="text-sm font-medium text-red-600">{error}</p>}

          {/* Action Buttons for Pending Review */}
          {isPendingReview && !editing && !escalating && (
            <div className="flex flex-col gap-3 md:flex-row">
              <button
                onClick={() => handleReview("approve")}
                disabled={isReviewing}
                className="rounded-md bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-700 disabled:opacity-50"
              >
                Approve
              </button>
              <button
                onClick={beginEdit}
                disabled={isReviewing}
                className="rounded-md bg-slate-200 px-4 py-2 text-slate-700 hover:bg-slate-300 disabled:opacity-50"
              >
                Edit
              </button>
              <button
                onClick={beginEscalate}
                disabled={isReviewing}
                className="rounded-md bg-amber-500 px-4 py-2 text-white hover:bg-amber-600 disabled:opacity-50"
              >
                Escalate
              </button>
            </div>
          )}

          {/* Save / Cancel Controls for Editing */}
          {editing && (
            <div className="flex flex-col gap-3 md:flex-row">
              <button
                onClick={() => handleReview("edit")}
                disabled={isReviewing || !editResolution.trim()}
                className="rounded-md bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700 disabled:opacity-50"
              >
                Save Resolution
              </button>
              <button
                onClick={cancelEdit}
                disabled={isReviewing}
                className="rounded-md bg-slate-200 px-4 py-2 text-slate-700 hover:bg-slate-300"
              >
                Cancel
              </button>
            </div>
          )}

          {/* Save / Cancel Controls for Escalating */}
          {escalating && (
            <div className="flex flex-col gap-3 md:flex-row">
              <button
                onClick={() => handleReview("escalate")}
                disabled={isReviewing || !escalationReason.trim()}
                className="rounded-md bg-amber-600 px-4 py-2 text-white hover:bg-amber-700 disabled:opacity-50"
              >
                Submit Escalation
              </button>
              <button
                onClick={cancelEscalate}
                disabled={isReviewing}
                className="rounded-md bg-slate-200 px-4 py-2 text-slate-700 hover:bg-slate-300"
              >
                Cancel
              </button>
            </div>
          )}

          <hr className="my-6 border-slate-200" />

          {/* Status Override Control */}
          <div>
            <h2 className="text-lg font-semibold">Manual Status Override</h2>
            <div className="mt-2 flex gap-3">
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                className="w-full max-w-xs rounded-md border border-slate-300 px-3 py-2"
              >
                <option value="OPEN">OPEN</option>
                <option value="PENDING_REVIEW">PENDING_REVIEW</option>
                <option value="RESOLVED">RESOLVED</option>
                <option value="ESCALATED">ESCALATED</option>
              </select>
              <button
                onClick={handleSaveStatus}
                className="rounded-md bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700"
              >
                Save Status
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}