from fastapi import FastAPI
import logging
import os
from alembic import command
from alembic.config import Config
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, projects, contacts, skill, blogs, mpesa, certificates, packages, portfolio_content

app = FastAPI()
logger = logging.getLogger(__name__)

@app.on_event("startup")
def run_database_migrations():
    """Bring a deployed database to the latest schema before serving requests."""
    try:
        config = Config(os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic.ini"))
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))
        command.upgrade(config, "heads")
        logger.info("Database migrations completed")
    except Exception:
        logger.exception("Database migration failed during startup")
        raise

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
