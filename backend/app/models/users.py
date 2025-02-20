from sqlmodel import SQLModel, Field, Relationship
from .orders import Orders
# Users table

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str | None = Field(default=None, index=True)
    password: str | None = None
    email: str | None = None
    phone: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    role: str | None = None
    created_at: str | None = None

