from sqlmodel import SQLModel

# Product model

class Productsbase(SQLModel):
    title: str
    description: str
    image_url: str
    unit_price: int
    sale_price: str
    is_active: bool
    status: str
    created_at: str
    updated_at: str

# Product input model

class ProductsCreate(Productsbase):
    title: str
    description: str
    unit_price: int
    sale_price: int
    is_active: bool
    status: str
    created_at: str
    updated_at: str

# Products Output model

class ProductsPublic(Productsbase):
    id: int
    category_id: int
    users_id: int
    title: str
    description: str
    unit_price: int
    sale_price: int
    is_active: bool
    status: str

#Products Update(Patch) model

class ProductUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    unit_price: int | None = None
    sale_price: int | None = None
    is_active: bool | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


