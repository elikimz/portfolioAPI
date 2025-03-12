# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from uuid import UUID

# from app.database import get_db
# from app.models import Skill, User
# from app.schema import SkillCreate, SkillUpdate, SkillResponse
# from app.routers.users import get_current_user

# router = APIRouter()


# # Create a new skill
# @router.post("", response_model=SkillResponse)
# def create_skill(
#     skill_data: SkillCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     new_skill = Skill(
#         **skill_data.dict(exclude={"user_id"}),
#         user_id=current_user.id
#     )
#     db.add(new_skill)
#     db.commit()
#     db.refresh(new_skill)
#     return new_skill


# # Get all skills for the current user
# @router.get("", response_model=List[SkillResponse])
# def get_skills(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     skills = db.query(Skill).filter(
#         Skill.user_id == current_user.id, Skill.is_deleted == False
#     ).all()
#     return skills


# # Get a single skill by ID
# @router.get("/{skill_id}", response_model=SkillResponse)
# def get_skill(
#     skill_id: UUID, 
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     skill = db.query(Skill).filter(
#         Skill.id == skill_id, Skill.user_id == current_user.id, Skill.is_deleted == False
#     ).first()

#     if not skill:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    
#     return skill


# # Update a skill
# @router.put("/{skill_id}", response_model=SkillResponse)
# def update_skill(
#     skill_id: UUID,
#     skill_update: SkillUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     skill = db.query(Skill).filter(
#         Skill.id == skill_id, Skill.user_id == current_user.id
#     ).first()

#     if not skill:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found or not authorized")

#     for key, value in skill_update.dict(exclude_unset=True).items():
#         setattr(skill, key, value)
    
#     db.commit()
#     db.refresh(skill)
#     return skill


# # Soft delete a skill
# @router.delete("/{skill_id}")
# def delete_skill(
#     skill_id: UUID, 
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     skill = db.query(Skill).filter(
#         Skill.id == skill_id, Skill.user_id == current_user.id
#     ).first()

#     if not skill:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found or not authorized")

#     skill.is_deleted = True
#     db.commit()

#     return {"message": "Skill deleted successfully"}


# # Let me know if you want any adjustments or more features! 🚀


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models import Skill, User
from app.schema import SkillCreate, SkillUpdate, SkillResponse
from app.routers.users import get_current_user

router = APIRouter()


# Create a new skill
@router.post("", response_model=SkillResponse)
def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_skill = Skill(
        **skill_data.dict(exclude={"user_id"}),
        user_id=current_user.id
    )
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill


# Get all skills (No authorization required)
@router.get("", response_model=List[SkillResponse])
def get_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).filter(Skill.is_deleted == False).all()
    return skills


# Get a single skill by ID (No authorization required)
@router.get("/{skill_id}", response_model=SkillResponse)
def get_skill(
    skill_id: UUID, 
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(
        Skill.id == skill_id, Skill.is_deleted == False
    ).first()

    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    
    return skill


# Update a skill
@router.put("/{skill_id}", response_model=SkillResponse)
def update_skill(
    skill_id: UUID,
    skill_update: SkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = db.query(Skill).filter(
        Skill.id == skill_id, Skill.user_id == current_user.id
    ).first()

    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found or not authorized")

    for key, value in skill_update.dict(exclude_unset=True).items():
        setattr(skill, key, value)
    
    db.commit()
    db.refresh(skill)
    return skill


# Soft delete a skill
@router.delete("/{skill_id}")
def delete_skill(
    skill_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = db.query(Skill).filter(
        Skill.id == skill_id, Skill.user_id == current_user.id
    ).first()

    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found or not authorized")

    skill.is_deleted = True
    db.commit()

    return {"message": "Skill deleted successfully"}


# Let me know if you want any adjustments or more features! 🚀