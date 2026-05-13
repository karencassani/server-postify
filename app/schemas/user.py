from datetime import datetime
import uuid
from sqlmodel import SQLModel

class UserCreate(SQLModel):
    username: str
    name: str
    lastname: str
    email: str
    password: str

class UserRead(SQLModel):
    id: uuid.UUID
    username: str
    name: str
    lastname: str
    email: str
    created_at: datetime

class UserUpdate(SQLModel):
    username: str | None = None
    name: str | None = None
    lastname: str | None = None
    email: str | None = None