# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from uuid import UUID

# from app.database import get_db
# from app.models import ContactMessage, User
# from app.schema import ContactMessageCreate, ContactMessageUpdate, ContactMessageResponse
# from app.routers.users import get_current_user

# router = APIRouter()


# # Create a new contact message
# @router.post("", response_model=ContactMessageResponse)
# def create_contact_message(
#     message_data: ContactMessageCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     new_message = ContactMessage(
#         **message_data.dict(exclude={"user_id"}),
#         user_id=current_user.id
#     )
#     db.add(new_message)
#     db.commit()
#     db.refresh(new_message)
#     return new_message


# # Get all contact messages
# @router.get("", response_model=List[ContactMessageResponse])
# def get_contact_messages(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     messages = db.query(ContactMessage).filter(
#         ContactMessage.user_id == current_user.id, ContactMessage.is_deleted == False
#     ).all()
#     return messages


# # Get a single contact message
# @router.get("/{message_id}", response_model=ContactMessageResponse)
# def get_contact_message(
#     message_id: UUID,  # Updated to UUID
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     message = db.query(ContactMessage).filter(
#         ContactMessage.id == message_id, ContactMessage.user_id == current_user.id, ContactMessage.is_deleted == False
#     ).first()

#     if not message:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact message not found")
    
#     return message


# # Update a contact message
# @router.put("/{message_id}", response_model=ContactMessageResponse)
# def update_contact_message(
#     message_id: UUID,
#     message_update: ContactMessageUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     message = db.query(ContactMessage).filter(
#         ContactMessage.id == message_id, ContactMessage.user_id == current_user.id
#     ).first()

#     if not message:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact message not found or not authorized")

#     for key, value in message_update.dict(exclude_unset=True).items():
#         setattr(message, key, value)
    
#     db.commit()
#     db.refresh(message)
#     return message


# # Soft delete a contact message
# @router.delete("/{message_id}")
# def delete_contact_message(
#     message_id: UUID,  # Updated to UUID
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     message = db.query(ContactMessage).filter(
#         ContactMessage.id == message_id, ContactMessage.user_id == current_user.id
#     ).first()

#     if not message:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact message not found or not authorized")

#     message.is_deleted = True
#     db.commit()

#     return {"message": "Contact message deleted successfully"}


# # Let me know if you want any changes! 🚀


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models import ContactMessage, User
from app.schema import ContactMessageCreate, ContactMessageUpdate, ContactMessageResponse
from app.routers.users import get_current_user

router = APIRouter()


# Create a new contact message (No authorization required)
@router.post("", response_model=ContactMessageResponse)
def create_contact_message(
    message_data: ContactMessageCreate,
    db: Session = Depends(get_db)
):
    new_message = ContactMessage(
        **message_data.dict()
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


# Get all contact messages (Authorization still required)
@router.get("", response_model=List[ContactMessageResponse])
def get_contact_messages(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    messages = db.query(ContactMessage).filter(
        ContactMessage.user_id == current_user.id, ContactMessage.is_deleted == False
    ).all()
    return messages


# Get a single contact message
@router.get("/{message_id}", response_model=ContactMessageResponse)
def get_contact_message(
    message_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = db.query(ContactMessage).filter(
        ContactMessage.id == message_id, ContactMessage.user_id == current_user.id, ContactMessage.is_deleted == False
    ).first()

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact message not found")
    
    return message


# Update a contact message
@router.put("/{message_id}", response_model=ContactMessageResponse)
def update_contact_message(
    message_id: UUID,
    message_update: ContactMessageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = db.query(ContactMessage).filter(
        ContactMessage.id == message_id, ContactMessage.user_id == current_user.id
    ).first()

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact message not found or not authorized")

    for key, value in message_update.dict(exclude_unset=True).items():
        setattr(message, key, value)
    
    db.commit()
    db.refresh(message)
    return message


# Soft delete a contact message
@router.delete("/{message_id}")
def delete_contact_message(
    message_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = db.query(ContactMessage).filter(
        ContactMessage.id == message_id, ContactMessage.user_id == current_user.id
    ).first()

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact message not found or not authorized")

    message.is_deleted = True
    db.commit()

    return {"message": "Contact message deleted successfully"}


# Let me know if you want me to make any more adjustments! 🚀
