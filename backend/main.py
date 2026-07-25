"""
FastAPI Contact Form Backend
Production-ready contact form API with email notifications and database storage.
"""

import logging
import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import settings
from models import Base, ContactMessage
from schemas import ContactFormRequest, ContactFormResponse
from email_service import send_contact_email
from rate_limiter import RateLimiter

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.ENVIRONMENT == "production" else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info(f"Starting FastAPI application (environment={settings.ENVIRONMENT})")
logger.info(f"Allowed CORS origins: {settings.ALLOWED_ORIGINS}")

# Initialize FastAPI app
app = FastAPI(
    title="Portfolio Contact API",
    description="Contact form backend for portfolio website",
    version="1.0.0"
)

# Configure CORS - MUST be added before route registration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Rate limiter
rate_limiter = RateLimiter(max_requests=5, window_seconds=3600)  # 5 requests per hour

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Portfolio Contact API is running", "status": "healthy"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/contact", response_model=ContactFormResponse)
async def submit_contact_form(
    request: Request,
    contact_data: ContactFormRequest,
    db: Session = Depends(get_db)
):
    """
    Submit a contact form message.
    
    - Validates input using Pydantic
    - Checks rate limiting
    - Stores in database
    - Sends email notification
    - Returns success/error response
    """
    try:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Check rate limiting
        if not rate_limiter.is_allowed(client_ip):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
        
        # Log submission attempt
        logger.info(f"Contact form submission from {client_ip}: {contact_data.email}")
        
        # Create database record
        db_message = ContactMessage(
            name=contact_data.name,
            email=contact_data.email,
            message=contact_data.message,
            ip_address=client_ip,
            submitted_at=datetime.utcnow(),
            status="received"
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        # Send email notification
        email_sent = await send_contact_email(
            name=contact_data.name,
            email=contact_data.email,
            message=contact_data.message,
            ip_address=client_ip
        )
        
        if email_sent:
            db_message.status = "email_sent"
            db.commit()
            logger.info(f"Email sent for submission ID: {db_message.id}")
        else:
            db_message.status = "email_failed"
            db.commit()
            logger.warning(f"Email failed for submission ID: {db_message.id}")
        
        return ContactFormResponse(
            success=True,
            message="Thank you for your message! I'll get back to you soon.",
            submission_id=db_message.id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request. Please try again."
        )
    finally:
        db.close()

@app.get("/api/submissions")
async def get_submissions(limit: int = 10, skip: int = 0, db: Session = Depends(get_db)):
    """Get recent contact form submissions (admin only in production)."""
    try:
        submissions = db.query(ContactMessage).order_by(
            ContactMessage.submitted_at.desc()
        ).offset(skip).limit(limit).all()
        
        return {
            "total": db.query(ContactMessage).count(),
            "submissions": [
                {
                    "id": s.id,
                    "name": s.name,
                    "email": s.email,
                    "message": s.message,
                    "status": s.status,
                    "submitted_at": s.submitted_at.isoformat(),
                    "ip_address": s.ip_address
                }
                for s in submissions
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching submissions: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching submissions")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=settings.DEBUG
    )
