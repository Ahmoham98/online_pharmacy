from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from models.products import Products
    from models.orders import Orders

# Order_items table

class OrderItems(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int | None = Field(default=None, foreign_key="products.id")
    orders_id: int | None = Field(default=None, foreign_key="orders.id")
    title: str
    description: str
    amount: int
    total_price: int
    created_at: str = Field(default="now")
    updated_at: str = Field(default="now")

    product: "Products" = Relationship(back_populates="order_item")
    order: "Orders" = Relationship(back_populates="order_item")

