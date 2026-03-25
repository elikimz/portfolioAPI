from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models import Certificate, User
from app.schema import CertificateCreate, CertificateUpdate, CertificateResponse
from app.routers.users import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CertificateResponse])
def get_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all certificates for the current user"""
    return db.query(Certificate).filter(
        Certificate.user_id == current_user.id,
        Certificate.is_deleted == False
    ).all()

@router.post("/", response_model=CertificateResponse)
def create_certificate(
    payload: CertificateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new certificate for the current user"""
    new_cert = Certificate(
        **payload.dict(),
        user_id=current_user.id
    )
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)
    return new_cert

@router.put("/{id}", response_model=CertificateResponse)
def update_certificate(
    id: UUID,
    payload: CertificateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a certificate (only the owner can update)"""
    cert = db.query(Certificate).filter(
        Certificate.id == id,
        Certificate.user_id == current_user.id,
        Certificate.is_deleted == False
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cert, key, value)
    
    db.commit()
    db.refresh(cert)
    return cert

@router.delete("/{id}")
def delete_certificate(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a certificate (only the owner can delete)"""
    cert = db.query(Certificate).filter(
        Certificate.id == id,
        Certificate.user_id == current_user.id,
        Certificate.is_deleted == False
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    cert.is_deleted = True
    db.commit()
    return {"message": "Certificate deleted successfully"}
