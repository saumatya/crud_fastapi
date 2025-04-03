from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = Column(DateTime(timezone=True), default=datetime.utcnow)
    disabled = Column(Boolean, default=False)
    name = Column(String, nullable=False)
    updated = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(String, nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="users")
    disabled = Column(Boolean, default=False)
    created = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )


Organization.users = relationship("User", back_populates="organization")

# Add the following lines to create the engine
DATABASE_URL = "postgresql://postgres:postgres@localhost/dashboard"
engine = create_engine(DATABASE_URL)

# Bind the engine to the Base's metadata
Base.metadata.create_all(bind=engine)
