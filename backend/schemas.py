"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class ContactFormRequest(BaseModel):
    """Schema for contact form submission."""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=5000)

    @validator('name')
    def validate_name(cls, v):
        """Sanitize name input."""
        v = v.strip()
        if not v or len(v) < 2:
            raise ValueError('Name must be at least 2 characters long')
        # Remove potential HTML/script tags
        if '<' in v or '>' in v or 'script' in v.lower():
            raise ValueError('Invalid characters in name')
        return v

    @validator('message')
    def validate_message(cls, v):
        """Sanitize message input."""
        v = v.strip()
        if not v or len(v) < 10:
            raise ValueError('Message must be at least 10 characters long')
        # Remove potential HTML/script tags
        if 'script' in v.lower():
            raise ValueError('Invalid content in message')
        return v

    class Config:
        """Pydantic config."""
        example = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "I'm interested in collaborating on a project..."
        }

class ContactFormResponse(BaseModel):
    """Schema for contact form response."""
    success: bool
    message: str
    submission_id: Optional[int] = None

    class Config:
        """Pydantic config."""
        example = {
            "success": True,
            "message": "Thank you for your message! I'll get back to you soon.",
            "submission_id": 1
        }

class SubmissionSchema(BaseModel):
    """Schema for contact message record."""
    id: int
    name: str
    email: str
    message: str
    status: str
    submitted_at: datetime
    ip_address: str

    class Config:
        """Pydantic config."""
        from_attributes = True
