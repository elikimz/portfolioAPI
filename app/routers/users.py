# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from datetime import timedelta

# from app.database import SessionLocal
# from app.models import User
# from app.schema import Token, UserLogin, UserCreate, UserUpdate
# from app.auth import decode_access_token, verify_password, create_access_token, hash_password
# from app.database import get_db

# router = APIRouter()
# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")




# # Register a new user
# @router.post("/register")
# def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.username == user_data.username).first()
#     if existing_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

#     new_user = User(
#         username=user_data.username,
#         password_hash=hash_password(user_data.password),
#         email=user_data.email,
#         full_name=user_data.full_name,
#         bio=user_data.bio,
#         profile_picture=user_data.profile_picture,
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {"message": "User registered successfully!"}

# # Login and get token
# @router.post("/token", response_model=Token)
# def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == form_data.username).first()

#     if not user or not verify_password(form_data.password, user.password_hash):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

#     access_token = create_access_token(data={"sub": user.username})

#     return {"access_token": access_token, "token_type": "bearer"}

# # Get current user from token
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     payload = decode_access_token(token)
#     if not payload or "sub" not in payload:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

#     username = payload["sub"]
#     user = db.query(User).filter(User.username == username, User.is_deleted == False).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

#     return user

# # Update user details
# @router.put("")
# def update_user_profile(user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     user = db.query(User).filter(User.id == current_user.id).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     if user_update.full_name is not None:
#         user.full_name = user_update.full_name
#     if user_update.bio is not None:
#         user.bio = user_update.bio
#     if user_update.profile_picture is not None:
#         user.profile_picture = user_update.profile_picture

#     db.commit()
#     db.refresh(user)

#     return {"message": "User profile updated successfully!"}


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

from app.database import SessionLocal
from app.models import User
from app.schema import Token, UserLogin, UserCreate, UserUpdate
from app.auth import decode_access_token, verify_password, create_access_token, hash_password
from app.database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


# Register a new user
@router.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    new_user = User(
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        email=user_data.email,
        full_name=user_data.full_name,
        bio=user_data.bio,
        profile_picture=user_data.profile_picture,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully!"}


# Login and get token
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


# Get all users
@router.get("/users")
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_db)):
    users = db.query(User).filter(User.is_deleted == False).all()
    return users


# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    username = payload["sub"]
    user = db.query(User).filter(User.username == username, User.is_deleted == False).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


# Update user details
@router.put("")
def update_user_profile(user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.bio is not None:
        user.bio = user_update.bio
    if user_update.profile_picture is not None:
        user.profile_picture = user_update.profile_picture

    db.commit()
    db.refresh(user)

    return {"message": "User profile updated successfully!"}


# Let me know if you want me to add filters, pagination, or anything else! 🚀