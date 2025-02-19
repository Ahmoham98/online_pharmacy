from sqlmodel import SQLModel, Field

class CategoriesBase(SQLModel):
    category_name: str
    description: str | None = None
    created_at: str

class Categories(CategoriesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category_name: str = Field(index=True)
    description: str | None = None
    created_at: str = Field(default="now")

class CategoriesCreate(CategoriesBase):
    created_at: str | None = None

class CategoriesPublic(CategoriesBase):
    id: int
    description: str | None = None

class CategoriesUpdate(CategoriesBase):
    id: int | None = None
    category_name: str | None = None
    description: str | None = None
    created_at: str | None = None

