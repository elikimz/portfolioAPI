


from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models import Project, User
from app.schema import ProjectCreate, ProjectUpdate, ProjectResponse
from app.routers.users import get_current_user

router = APIRouter()

# Create a new project
@router.post("", response_model=ProjectResponse)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_project = Project(
        **project_data.dict(),
        user_id=current_user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# Get all projects with pagination
@router.get("", response_model=List[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    offset = (page - 1) * size
    projects = db.query(Project).filter(Project.is_deleted == False).offset(offset).limit(size).all()
    return projects

# Get a single project
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: UUID, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.is_deleted == False).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

# Update a project
@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: UUID,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found or not authorized")

    for key, value in project_update.dict(exclude_unset=True).items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project

# Soft delete a project
@router.delete("/{project_id}")
def delete_project(project_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found or not authorized")

    project.is_deleted = True
    db.commit()

    return {"message": "Project deleted successfully"}
