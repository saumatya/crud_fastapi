from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from crud import (
    create_organization,
    get_organization,
    update_organization,
    delete_organization,
    get_all_organizations,
    create_user,
    get_user,
    update_user,
    delete_user,
    get_all_users,
)
from schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationOut,
    UserCreate,
    UserUpdate,
    User,
)
import uuid
from typing import List

DATABASE_URL = "postgresql://postgres:postgres@localhost/dashboard"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()

# Add CORS middleware to allow your frontend
origins = [
    "http://localhost:5173",  # Frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows your frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/organizations/", response_model=OrganizationOut)
def create_organization_endpoint(
    organization: OrganizationCreate, db: Session = Depends(get_db)
):
    return create_organization(db=db, organization=organization)


@app.get("/organizations/{organization_id}", response_model=OrganizationOut)
def get_organization_endpoint(
    organization_id: uuid.UUID, db: Session = Depends(get_db)
):
    db_organization = get_organization(db=db, organization_id=organization_id)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization


@app.get("/organizations/", response_model=List[OrganizationOut])
def get_all_organizations_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    organizations = get_all_organizations(db=db, skip=skip, limit=limit)
    return organizations


@app.put("/organizations/{organization_id}", response_model=OrganizationOut)
def update_organization_endpoint(
    organization_id: uuid.UUID,
    organization: OrganizationUpdate,
    db: Session = Depends(get_db),
):
    db_organization = update_organization(
        db=db, organization_id=organization_id, organization=organization
    )
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization


@app.delete("/organizations/{organization_id}", response_model=OrganizationOut)
def delete_organization_endpoint(
    organization_id: uuid.UUID, db: Session = Depends(get_db)
):
    db_organization = delete_organization(db=db, organization_id=organization_id)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization


# User Endpoints
@app.post("/users/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=User)
def get_user_endpoint(user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=List[User])
def get_all_users_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    users = get_all_users(db=db, skip=skip, limit=limit)
    return users


@app.put("/users/{user_id}", response_model=User)
def update_user_endpoint(
    user_id: uuid.UUID, user: UserUpdate, db: Session = Depends(get_db)
):
    db_user = update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=User)
def delete_user_endpoint(user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user = delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
