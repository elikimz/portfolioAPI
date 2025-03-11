from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from pydantic import HttpUrl



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = Field(None, min_length=3, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    profile_picture: Optional[str] = Field(None, max_length=255)

class UserLogin(BaseModel):
    Email: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    profile_picture: Optional[str] = Field(None, max_length=255)



from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class ProjectCreate(BaseModel):
    title: str
    description: str
    tech_stack: Optional[List[str]] = []
    github_link: Optional[str]
    live_link: Optional[str]
    image_url: Optional[str]
    category: Optional[str]
    tags: Optional[List[str]] = []
    is_featured: Optional[bool] = False
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class ProjectUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    tech_stack: Optional[List[str]]
    github_link: Optional[str]
    live_link: Optional[str]
    image_url: Optional[str]
    category: Optional[str]
    tags: Optional[List[str]]
    is_featured: Optional[bool]
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class ProjectResponse(BaseModel):
    id: UUID
    title: str
    description: str
    tech_stack: List[str]
    github_link: Optional[str]
    live_link: Optional[str]
    image_url: Optional[str]
    category: Optional[str]
    tags: List[str]
    is_featured: bool
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    user_id: UUID

    class Config:
        orm_mode = True


class ContactMessageCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    response: Optional[str] = None
    is_read: Optional[bool] = False
  


class ContactMessageUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    subject: Optional[str]
    message: Optional[str]
    response: Optional[str]
    is_read: Optional[bool]


class ContactMessageResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    subject: str
    message: str
    response: Optional[str]
    is_read: bool
    created_at: datetime
    is_deleted: bool
    user_id: UUID

    class Config:
        orm_mode = True





class ProficiencyLevel(str, Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"
    expert = "Expert"


class SkillCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    proficiency_level: ProficiencyLevel
    category: Optional[str] = Field(None, max_length=100)
    icon_url: Optional[str]


class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    proficiency_level: Optional[ProficiencyLevel]
    category: Optional[str] = Field(None, max_length=100)
    icon_url: Optional[str]


class SkillResponse(BaseModel):
    id: UUID
    name: str
    proficiency_level: ProficiencyLevel
    category: Optional[str]
    icon_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    user_id: UUID

    class Config:
        orm_mode = True



class BlogPostCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []
    category: Optional[str]

class BlogPostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    tags: Optional[List[str]]
    category: Optional[str]

class BlogPostResponse(BaseModel):
    id: UUID
    title: str
    content: str
    author_id: UUID
    published_at: datetime
    tags: List[str]
    category: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        orm_mode = True


# Let me know if you want me to tweak anything! 🚀
