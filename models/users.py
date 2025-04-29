from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

if TYPE_CHECKING:
    from models.orders import Orders
    from models.products import Products

# Users table

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str | None = Field(default=None, index=True)
    hashed_password: str | None = None
    email: EmailStr | None = None
    phone: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    role: str | None = None
    created_at: str | None = None
    is_superuser: bool | None = False

    orders: list["Orders"] = Relationship(back_populates="users")
    products: list["Products"] = Relationship(back_populates="users")