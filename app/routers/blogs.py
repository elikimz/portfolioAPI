from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models import BlogPost, User
from app.schema import BlogPostCreate, BlogPostUpdate, BlogPostResponse
from app.routers.users import get_current_user

router = APIRouter()

# Create a blog post
@router.post("", response_model=BlogPostResponse)
def create_blog_post(
    post_data: BlogPostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_post = BlogPost(
        **post_data.dict(),
        author_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get all blog posts
@router.get("", response_model=List[BlogPostResponse])
def get_blog_posts(db: Session = Depends(get_db)):
    posts = db.query(BlogPost).filter(BlogPost.is_deleted == False).all()
    return posts

# Get a single blog post
@router.get("/{post_id}", response_model=BlogPostResponse)
def get_blog_post(post_id: UUID, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id, BlogPost.is_deleted == False).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")
    return post

# Update a blog post
@router.put("/{post_id}", response_model=BlogPostResponse)
def update_blog_post(
    post_id: UUID,
    post_update: BlogPostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(BlogPost).filter(BlogPost.id == post_id, BlogPost.author_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found or not authorized")

    for key, value in post_update.dict(exclude_unset=True).items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post

# Soft delete a blog post
@router.delete("/{post_id}")
def delete_blog_post(post_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id, BlogPost.author_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found or not authorized")

    post.is_deleted = True
    db.commit()

    return {"message": "Blog post deleted successfully"}
