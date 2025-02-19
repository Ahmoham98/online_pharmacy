from sqlmodel import SQLModel, Field

# Products table

class Products(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category_id: int | None = Field(default=None, foreign_key="categories.id")
    users_id: int | None = Field(default=None, foreign_key="users.id")
    title: str | None = None
    description: str | None = None
    image_url: str
    unit_price: int
    sale_price: int | None = None
    is_active: bool = Field(default=True)
    status: str | None = None 
    created_at: str | None = None
    updated_at: str | None = None

