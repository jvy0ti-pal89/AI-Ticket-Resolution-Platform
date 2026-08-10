import logging
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketReviewRequest, TicketUpdate
from app.models.user import User
from app.services.ai_service import enrich_ticket_with_ai

logger = logging.getLogger(__name__)


# 1. CREATE TICKET
def create_ticket(db: Session, ticket_in: TicketCreate, user: User) -> Ticket:
    ticket = Ticket(
        title=ticket_in.title,
        description=ticket_in.description,
        priority=(
            ticket_in.priority
            if isinstance(ticket_in.priority, str)
            else (getattr(ticket_in.priority, "value", "Medium"))
        ),
        category=ticket_in.category,
        user_id=user.id,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # Safely trigger AI enrichment
    try:
        enrich_ticket_with_ai(db, ticket)
        db.commit()
        db.refresh(ticket)
    except Exception as e:
        logger.error(f"AI enrichment failed for ticket #{ticket.id}: {str(e)}")

    return ticket


# 2. GET ALL TICKETS (MISSING PIECE)
def get_tickets(db: Session, skip: int = 0, limit: int = 100) -> List[Ticket]:
    return db.query(Ticket).offset(skip).limit(limit).all()


# 3. GET SINGLE TICKET BY ID (MISSING PIECE)
def get_ticket_by_id(db: Session, ticket_id: int) -> Optional[Ticket]:
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


# 4. UPDATE TICKET (MISSING PIECE)
def update_ticket(
    db: Session, ticket_id: int, ticket_update: TicketUpdate
) -> Optional[Ticket]:
    db_ticket = get_ticket_by_id(db, ticket_id)
    if not db_ticket:
        return None

    update_data = ticket_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ticket, key, value)

    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def review_ticket(
    db: Session,
    ticket_id: int,
    review_request: TicketReviewRequest,
    reviewer: User,
) -> Optional[Ticket]:
    db_ticket = get_ticket_by_id(db, ticket_id)
    if not db_ticket:
        return None

    now = datetime.utcnow()
    action = review_request.action

    if action == "approve":
        db_ticket.status = "RESOLVED"
    elif action == "edit":
        db_ticket.resolution = review_request.resolution
        db_ticket.status = "RESOLVED"
    elif action == "escalate":
        db_ticket.status = "ESCALATED"
        db_ticket.escalation_reason = (
            review_request.escalation_reason
            or "AI recommendation deemed insufficient. Escalated for further investigation."
        )

    db_ticket.reviewed_by_id = reviewer.id
    db_ticket.reviewed_at = now

    db.commit()
    db.refresh(db_ticket)
    return db_ticket


# 5. DELETE TICKET (MISSING PIECE)
def delete_ticket(db: Session, ticket_id: int) -> bool:
    db_ticket = get_ticket_by_id(db, ticket_id)
    if not db_ticket:
        return False
    db.delete(db_ticket)
    db.commit()
    return True
