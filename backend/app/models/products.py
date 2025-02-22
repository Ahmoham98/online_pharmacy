from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from ..models.users import Users
    from ..models.categories import Categories
    from ..models.order_items import OrderItems

# Products table

class Products(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category_id: int | None = Field(default=None, foreign_key="categories.id")
    users_id: int | None = Field(default=None, foreign_key="users.id")
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    unit_price: int | None = None
    sale_price: int | None = None
    is_active: bool = Field(default=True)
    status: str | None = None 
    created_at: str | None = None
    updated_at: str | None = None

    users: "Users" = Relationship(back_populates="products")
    category: "Categories" = Relationship(back_populates="products")
    order_item: "OrderItems" = Relationship(back_populates="product")
