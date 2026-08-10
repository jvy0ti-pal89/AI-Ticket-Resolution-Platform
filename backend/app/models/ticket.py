from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, default="OPEN")  # OPEN, PENDING_REVIEW, RESOLVED, ESCALATED
    category = Column(String, nullable=True)  # Populated later via AI
    priority = Column(String, nullable=True)  # Populated later via AI
    summary = Column(Text, nullable=True)  # Populated later via AI
    resolution = Column(Text, nullable=True)  # Grounded AI resolution from RAG
    reviewed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    escalation_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationship back to User
    owner = relationship(
        "User", foreign_keys=[user_id], back_populates="created_tickets"
    )
    assignee = relationship(
        "User", foreign_keys=[assigned_to_id], back_populates="assigned_tickets"
    )
    reviewer = relationship("User", foreign_keys=[reviewed_by_id])
