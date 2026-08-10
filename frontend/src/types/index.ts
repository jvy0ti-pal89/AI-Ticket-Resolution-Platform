export interface User {
  id: number;
  email: string;
  full_name: string;
  role: "admin" | "engineer" | "employee";
}

export interface Ticket {
  id: number;
  title: string;
  description: string;
  status: string;
  category?: string;
  priority?: string;
  summary?: string;
  resolution?: string;
  reviewed_by_id?: number | null;
  reviewed_at?: string | null;
  escalation_reason?: string | null;
  created_at: string;
  user_id: number;
  assigned_to_id?: number | null;
}

export interface DashboardMetrics {
  total_tickets: number;
  open_tickets: number;
  pending_review: number;
  resolved_tickets: number;
  escalated_tickets: number;
  high_priority_tickets: number;
  category_breakdown: Array<{ category: string; count: number }>;
  recent_tickets: Array<Pick<Ticket, "id" | "title" | "category" | "priority" | "status" | "summary" | "created_at">>;
  high_priority_ticket_list: Array<Pick<Ticket, "id" | "title" | "category" | "priority" | "status" | "summary" | "created_at">>;
}
