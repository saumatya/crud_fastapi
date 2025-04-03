from sqlalchemy.orm import Session
from models import Organization, User
from schemas import OrganizationCreate, OrganizationUpdate, UserCreate, UserUpdate


def create_organization(db: Session, organization: OrganizationCreate):
    db_organization = Organization(
        name=organization.name, disabled=organization.disabled
    )
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization


def get_organization(db: Session, organization_id: str):
    return db.query(Organization).filter(Organization.id == organization_id).first()


def update_organization(
    db: Session, organization_id: str, organization: OrganizationUpdate
):
    db_organization = (
        db.query(Organization).filter(Organization.id == organization_id).first()
    )
    if db_organization:
        if organization.name:
            db_organization.name = organization.name
        if organization.disabled is not None:
            db_organization.disabled = organization.disabled
        db.commit()
        db.refresh(db_organization)
        return db_organization
    return None


def delete_organization(db: Session, organization_id: str):
    db_organization = (
        db.query(Organization).filter(Organization.id == organization_id).first()
    )
    if db_organization:
        db.delete(db_organization)
        db.commit()
        return db_organization
    return None


def get_all_organizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Organization).offset(skip).limit(limit).all()


# User CRUD
def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        phone=user.phone,
        role=user.role,
        organization_id=user.organization_id,
        disabled=user.disabled,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: str, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if user.name:
            db_user.name = user.name
        if user.email:
            db_user.email = user.email
        if user.phone:
            db_user.phone = user.phone
        if user.role:
            db_user.role = user.role
        if user.disabled is not None:
            db_user.disabled = user.disabled
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db: Session, user_id: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
