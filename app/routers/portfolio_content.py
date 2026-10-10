from typing import List, Type
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Experience, Achievement, EventPhoto
from app.schema import ExperienceCreate, ExperienceResponse, AchievementCreate, AchievementResponse, EventPhotoCreate, EventPhotoResponse
from app.routers.users import get_current_user

router = APIRouter()

def collection(model: Type, response_model, create_model, path: str):
    @router.get(path, response_model=List[response_model])
    def list_items(db: Session = Depends(get_db)):
        return db.query(model).filter(model.is_deleted == False).order_by(model.created_at.desc()).all()
    @router.post(path, response_model=response_model, status_code=201)
    def create_item(payload: create_model, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        item = model(**payload.model_dump(), user_id=current_user.id)
        db.add(item); db.commit(); db.refresh(item); return item
    @router.put(f"{path}/{{item_id}}", response_model=response_model)
    def update_item(item_id: UUID, payload: create_model, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        item = db.query(model).filter(model.id == item_id, model.user_id == current_user.id, model.is_deleted == False).first()
        if not item: raise HTTPException(status_code=404, detail="Item not found")
        for key, value in payload.model_dump(exclude_unset=True).items(): setattr(item, key, value)
        db.commit(); db.refresh(item); return item
    @router.delete(f"{path}/{{item_id}}")
    def delete_item(item_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        item = db.query(model).filter(model.id == item_id, model.user_id == current_user.id, model.is_deleted == False).first()
        if not item: raise HTTPException(status_code=404, detail="Item not found")
        item.is_deleted = True; db.commit(); return {"message": "Item deleted successfully"}

collection(Experience, ExperienceResponse, ExperienceCreate, "/experiences")
collection(Achievement, AchievementResponse, AchievementCreate, "/achievements")
collection(EventPhoto, EventPhotoResponse, EventPhotoCreate, "/event-photos")
