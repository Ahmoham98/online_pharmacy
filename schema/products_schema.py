from sqlmodel import SQLModel, Field

# Product model

class Productsbase(SQLModel):
    title: str
    description: str
    image_url: str
    unit_price: int
    sale_price: int
    is_active: bool
    status: str
    created_at: str = Field(default="now")
    updated_at: str = Field(default="now")

# Product input model
class ProductsCreate(Productsbase):
    pass

# Products Output model
class ProductsPublic(Productsbase):
    id: int
    category_id: int
    users_id: int


#Products Update(Patch) model
class ProductUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    unit_price: int | None = None
    sale_price: int | None = None
    is_active: bool | None = None
    status: str | None = None
    created_at: str = Field(default="now")
    updated_at: str = Field(default="now")


