from sqlmodel import SQLModel, Field

# Order_items model

class OrderItemsBase(SQLModel):
    title: str
    description: str
    created_at: str = Field(default="now")
    updated_at: str = Field(default="now")

# Order_items Input model

class OrderItemsCreate(OrderItemsBase):
    amount: int
    status: str


# Order_items Output model

class OrderItemsPublic(OrderItemsBase):
    id: int
    products_id: int
    orders_id: int
    amount: int
    total_price: int
    status: str

# Order_items Update(Patch) model

class OrderItemsUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    unit_price: int | None = None
    sale_price: int | None = None
    is_active: bool | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


