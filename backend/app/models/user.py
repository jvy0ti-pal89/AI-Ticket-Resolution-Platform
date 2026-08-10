from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    full_name = Column(String(256), nullable=False)
    hashed_password = Column(String(256), nullable=False)
    role = Column(String(50), default="employee", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    created_tickets = relationship(
        "Ticket", foreign_keys="Ticket.user_id", back_populates="owner"
    )
    assigned_tickets = relationship(
        "Ticket", foreign_keys="Ticket.assigned_to_id", back_populates="assignee"
    )

    documents = relationship(
        "Document",
        back_populates="uploaded_by",
        cascade="all, delete-orphan",
    )
