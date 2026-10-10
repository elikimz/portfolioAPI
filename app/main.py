from fastapi import FastAPI
import logging
import os
from sqlalchemy import inspect, text
from app.database import engine
from app.models import Experience, Achievement, EventPhoto
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, projects, contacts, skill, blogs, mpesa, certificates, packages, portfolio_content

app = FastAPI()
logger = logging.getLogger(__name__)
app.state.release = "mpesa-status-v1"

@app.on_event("startup")
def ensure_portfolio_schema():
    """Create only the additive portfolio fields/tables needed by this release."""
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS cv_url VARCHAR"))
        connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS cv_filename VARCHAR"))
        connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS cv_updated_at TIMESTAMP"))
        Experience.__table__.create(connection, checkfirst=True)
        Achievement.__table__.create(connection, checkfirst=True)
        EventPhoto.__table__.create(connection, checkfirst=True)
        logger.info("Portfolio schema is ready")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With"],
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
app.include_router(skill.router, prefix="/skill", tags=["Skill"])
app.include_router(blogs.router, prefix="/blogs", tags=["Blogs"])
app.include_router(mpesa.router, prefix="/mpesa", tags=["M-Pesa"])
app.include_router(certificates.router, prefix="/certificates", tags=["Certificates"])
app.include_router(packages.router, prefix="/packages", tags=["Packages"])
app.include_router(portfolio_content.router, tags=["Portfolio content"])

@app.get("/")
def read_root():
    return {"message": "Welcome to my portfolio API!"}
