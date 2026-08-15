from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user_dependency, get_db_dependency
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ticket import (
    TicketCreate,
    TicketResponse,
    TicketReviewRequest,
    TicketUpdate,
)
from app.security.roles import (
    ensure_can_create_ticket,
    ensure_can_modify_ticket,
    ensure_can_review_ticket,
    ensure_can_view_ticket,
)
from app.services import ticket_service

# Set prefix and tags for clean Swagger UI categorization
router = APIRouter(prefix="/tickets", tags=["Tickets"])


# ----------------------------------------------------
# 1. CREATE TICKET
# ----------------------------------------------------
@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket_endpoint(
    ticket_in: TicketCreate,
    db: Session = Depends(get_db_dependency),
    current_user: User = Depends(get_current_user_dependency),
) -> TicketResponse:
    """
    Creates a new support ticket and automatically enriches it with AI categorization.
    """
    ensure_can_create_ticket(current_user)
    ticket = ticket_service.create_ticket(db=db, ticket_in=ticket_in, user=current_user)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create ticket",
        )
    return ticket


# ----------------------------------------------------
# # ----------------------------------------------------
# 2. READ ALL TICKETS
# ----------------------------------------------------
@router.get("", response_model=List[TicketResponse], status_code=status.HTTP_200_OK)
def read_tickets_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_dependency),
    current_user: User = Depends(get_current_user_dependency),
) -> List[TicketResponse]:
    """
    Retrieves a list of tickets with pagination support based on user roles.
    """
    user_role = str(current_user.role).lower()

    if user_role == "admin":
        return ticket_service.get_tickets(db, skip=skip, limit=limit)

    if user_role == "engineer":
        return (
            db.query(Ticket)
            .filter(Ticket.status == "PENDING_REVIEW")
            .offset(skip)
            .limit(limit)
            .all()
        )


# ----------------------------------------------------
# 3. READ SINGLE TICKET BY ID
# ----------------------------------------------------
@router.get(
    "/{ticket_id}", response_model=TicketResponse, status_code=status.HTTP_200_OK
)
def read_ticket_endpoint(
    ticket_id: int,
    db: Session = Depends(get_db_dependency),
    current_user: User = Depends(get_current_user_dependency),
) -> TicketResponse:
    """
    Retrieves details of a specific ticket by ID.
    """
    ticket = ticket_service.get_ticket_by_id(db, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} not found",
        )
    ensure_can_view_ticket(current_user, ticket)
    return ticket


# ----------------------------------------------------
# 4. UPDATE TICKET
# ----------------------------------------------------
@router.put(
    "/{ticket_id}", response_model=TicketResponse, status_code=status.HTTP_200_OK
)
def update_ticket_endpoint(
    ticket_id: int,
    ticket_update: TicketUpdate,
    db: Session = Depends(get_db_dependency),
    current_user: User = Depends(get_current_user_dependency),
) -> TicketResponse:
    """
    Updates an existing ticket's information or status.
    """
    ticket = ticket_service.get_ticket_by_id(db, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} not found",
        )
    ensure_can_modify_ticket(current_user, ticket)
    updated_ticket = ticket_service.update_ticket(
        db, ticket_id=ticket_id, ticket_update=ticket_update
    )
    return updated_ticket


# ----------------------------------------------------
# 5. REVIEW TICKET
# ----------------------------------------------------
@router.post(
    "/{ticket_id}/review",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
)
def review_ticket_endpoint(
    ticket_id: int,
    review_request: TicketReviewRequest,
    db: Session = Depends(get_db_dependency),
    current_user: User = Depends(get_current_user_dependency),
) -> TicketResponse:
    """
    Review an AI-generated ticket recommendation.
    Approve, edit, or escalate the ticket resolution.
    """
    ticket = ticket_service.get_ticket_by_id(db, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} not found",
        )
    ensure_can_review_ticket(current_user, ticket)

    # Payload validation checks
    if review_request.action == "edit" and not review_request.resolution:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resolution content is required for edit action.",
        )

    if review_request.action == "escalate" and not review_request.escalation_reason:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Escalation reason is required for escalate action.",
        )

    reviewed_ticket = ticket_service.review_ticket(
        db=db, ticket_id=ticket_id, review_request=review_request, reviewer=current_user
    )
    if not reviewed_ticket:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to review ticket",
        )
    return reviewed_ticket


# ----------------------------------------------------
# 6. DELETE TICKET
# ----------------------------------------------------
@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket_endpoint(
    ticket_id: int,
    db: Session = Depends(get_db_dependency),
    current_user: User = Depends(get_current_user_dependency),
) -> None:
    """
    Deletes a ticket by ID.
    """
    success = ticket_service.delete_ticket(db, ticket_id=ticket_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} not found",
        )
    return None
