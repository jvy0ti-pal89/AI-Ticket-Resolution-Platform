from typing import Any, Dict, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.user import User


def _ticket_query_for_user(db: Session, user: User):
    query = db.query(Ticket)
    if user.role == "admin":
        return query

    if user.role == "engineer":
        return query.filter(Ticket.assigned_to_id == user.id)

    return query.filter(Ticket.user_id == user.id)


def get_dashboard_metrics(db: Session, user: User) -> Dict[str, Any]:
    query = _ticket_query_for_user(db, user)

    total = query.count()
    open_tickets = query.filter(Ticket.status == "OPEN").count()
    pending_review = query.filter(Ticket.status == "PENDING_REVIEW").count()
    resolved = query.filter(Ticket.status == "RESOLVED").count()
    escalated = query.filter(Ticket.status == "ESCALATED").count()
    high_priority = query.filter(func.lower(Ticket.priority) == "high").count()

    category_rows = (
        query.with_entities(Ticket.category, func.count(Ticket.id))
        .group_by(Ticket.category)
        .all()
    )
    category_breakdown: List[Dict[str, Any]] = [
        {"category": category or "Uncategorized", "count": count}
        for category, count in category_rows
    ]

    recent_tickets = query.order_by(Ticket.created_at.desc()).limit(5).all()

    high_priority_tickets = (
        query.filter(func.lower(Ticket.priority) == "high")
        .order_by(Ticket.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "total_tickets": total,
        "open_tickets": open_tickets,
        "pending_review": pending_review,
        "resolved_tickets": resolved,
        "escalated_tickets": escalated,
        "high_priority_tickets": high_priority,
        "category_breakdown": category_breakdown,
        "recent_tickets": [
            {
                "id": ticket.id,
                "title": ticket.title,
                "category": ticket.category,
                "priority": ticket.priority,
                "status": ticket.status,
                "summary": ticket.summary,
                "created_at": ticket.created_at,
            }
            for ticket in recent_tickets
        ],
        "high_priority_ticket_list": [
            {
                "id": ticket.id,
                "title": ticket.title,
                "category": ticket.category,
                "priority": ticket.priority,
                "status": ticket.status,
                "summary": ticket.summary,
                "created_at": ticket.created_at,
            }
            for ticket in high_priority_tickets
        ],
    }
