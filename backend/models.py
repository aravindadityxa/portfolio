"""
SQLAlchemy database models.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ContactMessage(Base):
    """Database model for contact form submissions."""
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    message = Column(Text, nullable=False)
    ip_address = Column(String(50), nullable=True)
    status = Column(String(50), default="received", nullable=False)  # received, email_sent, email_failed
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    read = Column(Boolean, default=False)

    def __repr__(self):
        return f"<ContactMessage(id={self.id}, name={self.name}, email={self.email}, status={self.status})>"
