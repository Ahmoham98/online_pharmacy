from sqlmodel import SQLModel, Field

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



