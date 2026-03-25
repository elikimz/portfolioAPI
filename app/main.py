from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, projects, contacts, skill, blogs, mpesa, certificates

app = FastAPI()

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

@app.get("/")
def read_root():
    return {"message": "Welcome to my portfolio API!"}
