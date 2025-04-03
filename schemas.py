from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
import uuid
from uuid import UUID


class OrganizationCreate(BaseModel):
    name: str
    disabled: Optional[bool] = False


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    disabled: Optional[bool] = None


class OrganizationOut(OrganizationCreate):
    id: uuid.UUID
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str
    disabled: Optional[bool] = False


class UserCreate(UserBase):
    password: str
    organization_id: UUID


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    disabled: Optional[bool] = None


class User(UserBase):
    id: UUID
    organization_id: UUID
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True
