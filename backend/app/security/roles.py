from fastapi import HTTPException, status
from app.models.user import User
from app.models.ticket import Ticket

ADMIN = "admin"
ENGINEER = "engineer"
EMPLOYEE = "employee"


def ensure_can_create_ticket(user: User) -> None:
    if user.role not in {EMPLOYEE, ADMIN}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to create tickets",
        )


def ensure_is_admin(user: User) -> None:
    if user.role != ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative access required",
        )


def ensure_can_view_ticket(user: User, ticket: Ticket) -> None:
    if user.role == ADMIN:
        return
    if user.role == ENGINEER and ticket.assigned_to_id == user.id:
        return
    if user.role == EMPLOYEE and ticket.user_id == user.id:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User does not have permission to view this ticket",
    )


def ensure_can_modify_ticket(user: User, ticket: Ticket) -> None:
    if user.role == ADMIN:
        return
    if user.role == ENGINEER and ticket.assigned_to_id == user.id:
        return
    if user.role == EMPLOYEE and ticket.user_id == user.id:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User does not have permission to modify this ticket",
    )


def ensure_can_review_ticket(user: User, ticket: Ticket) -> None:
    if user.role == ADMIN:
        return
    if user.role == ENGINEER and ticket.assigned_to_id == user.id:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User does not have permission to review this ticket",
    )
