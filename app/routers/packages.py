"""Packages router — CRUD for website service packages."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update, desc
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Package, User
from app.schema import PackageCreate, PackageUpdate, PackageResponse
from app.routers.users import get_current_user

router = APIRouter(tags=["Packages"])


# ── Public: List active packages ─────────────────────────────────────────────

@router.get("", response_model=List[PackageResponse])
def list_packages(
    page: int = 1,
    size: int = 50,
    db: Session = Depends(get_db),
):
    """Public endpoint — returns active, non-deleted packages sorted by display_order."""
    skip = (page - 1) * size
    stmt = (
        select(Package)
        .where(Package.is_active == True, Package.is_deleted == False)
        .order_by(Package.display_order.asc(), Package.created_at.desc())
        .offset(skip)
        .limit(size)
    )
    results = db.execute(stmt).scalars().all()
    return results


@router.get("/{package_id}", response_model=PackageResponse)
def get_package(package_id: UUID, db: Session = Depends(get_db)):
    """Public endpoint — returns a single package by ID."""
    stmt = select(Package).where(
        Package.id == package_id,
        Package.is_active == True,
        Package.is_deleted == False,
    )
    package = db.execute(stmt).scalars().first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package


# ── Authenticated: Create package ────────────────────────────────────────────

@router.post("", response_model=PackageResponse, status_code=status.HTTP_201_CREATED)
def create_package(
    payload: PackageCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Admin endpoint — create a new service package."""
    package = Package(
        **payload.dict(),
        user_id=current_user.id,
    )
    db.add(package)
    db.commit()
    db.refresh(package)
    return package


# ── Authenticated: Update package ────────────────────────────────────────────

@router.put("/{package_id}", response_model=PackageResponse)
def update_package(
    package_id: UUID,
    payload: PackageUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Admin endpoint — update an existing service package."""
    stmt = select(Package).where(
        Package.id == package_id,
        Package.user_id == current_user.id,
        Package.is_deleted == False,
    )
    package = db.execute(stmt).scalars().first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(package, key, value)

    db.commit()
    db.refresh(package)
    return package


# ── Authenticated: Delete package (soft) ─────────────────────────────────────

@router.delete("/{package_id}", status_code=status.HTTP_200_OK)
def delete_package(
    package_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Admin endpoint — soft delete a package."""
    stmt = select(Package).where(
        Package.id == package_id,
        Package.user_id == current_user.id,
        Package.is_deleted == False,
    )
    package = db.execute(stmt).scalars().first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    package.is_deleted = True
    db.commit()
    return {"message": "Package deleted successfully"}
