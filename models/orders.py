from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from ..models.users import Users
    from ..models.order_items import OrderItems

# Orders table
    
class Orders(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    users_id: int | None = Field(default=None, foreign_key="users.id")
    total_price: int | None = None
    card_number: int | None = None
    card_expiration_date: int | None = None
    email: str | None = None
    phone: int | None = None
    address: str | None = None
    coupon: str | None = None
    discount: int | None = None
    status: str| None = None
    created_at: str = Field(default="now")
    updated_at: str = Field(default="now")

    users: "Users" = Relationship(back_populates="orders")
    order_item: "OrderItems" = Relationship(back_populates="order")
