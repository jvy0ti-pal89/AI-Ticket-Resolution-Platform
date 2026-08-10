import api from "./api";
import type { Ticket } from "../types";

export async function fetchTickets() {
  const response = await api.get<Ticket[]>("/tickets/");
  return response.data;
}

export async function fetchTicket(ticketId: number) {
  const response = await api.get<Ticket>(`/tickets/${ticketId}`);
  return response.data;
}

export async function createTicket(ticket: Partial<Ticket>) {
  const response = await api.post<Ticket>("/tickets/", ticket);
  return response.data;
}

export async function updateTicket(ticketId: number, data: Partial<Ticket>) {
  const response = await api.put<Ticket>(`/tickets/${ticketId}`, data);
  return response.data;
}

export async function reviewTicket(
  ticketId: number,
  data: {
    action: "approve" | "edit" | "escalate";
    resolution?: string;
    escalation_reason?: string;
  }
) {
  const response = await api.post<Ticket>(`/tickets/${ticketId}/review`, data);
  return response.data;
}