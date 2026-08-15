from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, root_validator


# 1. Base Schema (shared fields)
class TicketBase(BaseModel):
    title: str
    description: str


# 2. Schema for creating a ticket
class TicketCreate(TicketBase):
    priority: Optional[str] = "Medium"
    category: Optional[str] = None


# 3. Schema for updating an existing ticket (MISSING PIECE)
class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    summary: Optional[str] = None
    resolution: Optional[str] = None
    escalation_reason: Optional[str] = None


class TicketReviewRequest(BaseModel):
    action: Literal["approve", "edit", "escalate"]
    resolution: Optional[str] = None
    escalation_reason: Optional[str] = None

    @root_validator(skip_on_failure=True)
    def validate_review_request(cls, values):
        action = values.get("action")
        resolution = values.get("resolution")
        if action == "edit" and not resolution:
            raise ValueError("resolution is required when action is 'edit'")
        return values


# 4. Schema for returning a ticket response
class TicketResponse(TicketBase):
    id: int
    status: str
    category: Optional[str] = None
    priority: Optional[str] = None
    summary: Optional[str] = None
    resolution: Optional[str] = None
    reviewed_by_id: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    escalation_reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
