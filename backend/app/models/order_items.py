from sqlmodel import SQLModel, Field

# defining order_items base model

class OrderItemsBase(SQLModel):
    title: str
    description: str
    created_at: str = Field(default="now")
    updated_at: str = Field(default="now")

# define order_items table

class OrderItems(OrderItemsBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int | None = Field(default=None, foreign_key="products.id")
    orders_id: int | None = Field(default=None, foreign_key="orders.id")
    
    amount: int
    total_price: int

# define order_items input model

class OrderItemsCreate(OrderItemsBase):
    amount: int
    status: str


# define order_items output model

class OrderItemsPublic(OrderItemsBase):
    id: int
    products_id: int
    orders_id: int
    amount: int
    total_price: int
    status: str

# define order_items update model

class OrderItemsUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    unit_price: int | None = None
    sale_price: int | None = None
    is_active: bool | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


