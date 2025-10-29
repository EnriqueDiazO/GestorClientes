
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Role(str):
    CLIENTE = "CLIENTE"
    ADMIN_1 = "ADMIN_1"
    ADMIN_2 = "ADMIN_2"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    role: str = Field(default=Role.CLIENTE)

class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    filename: str
    stored_path: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    content_type: Optional[str] = None
    size_bytes: Optional[int] = None
