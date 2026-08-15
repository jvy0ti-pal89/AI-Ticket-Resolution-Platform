import api from "./api";
import type { Ticket } from "../types";

// Explicit type for review payload
export interface ReviewPayload {
  action: "approve" | "edit" | "escalate";
  resolution?: string;
  escalation_reason?: string;
}

export async function fetchTickets(): Promise<Ticket[]> {
  const response = await api.get<Ticket[]>("/tickets");
  return response.data;
}

export async function fetchTicket(ticketId: number): Promise<Ticket> {
  const response = await api.get<Ticket>(`/tickets/${ticketId}`);
  return response.data;
}

export async function createTicket(ticket: Partial<Ticket>): Promise<Ticket> {
  const response = await api.post<Ticket>("/tickets", ticket);
  return response.data;
}

export async function updateTicket(
  ticketId: number,
  data: Partial<Ticket>
): Promise<Ticket> {
  const response = await api.put<Ticket>(`/tickets/${ticketId}`, data);
  return response.data;
}

export async function reviewTicket(
  ticketId: number,
  data: ReviewPayload
): Promise<Ticket> {
  const response = await api.post<Ticket>(`/tickets/${ticketId}/review`, data);
  return response.data;
}