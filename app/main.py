from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, projects, contacts, skill, blogs

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],  # Replace "*" with your frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
app.include_router(skill.router, prefix="/skill", tags=["Skill"])
app.include_router(blogs.router, prefix="/blogs", tags=["Blogs"])

@app.get("/")
def read_root():
    return {"message": "Welcome to my portfolio API!"}
