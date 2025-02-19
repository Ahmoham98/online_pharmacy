from sqlmodel import SQLModel, Field

class CategoriesBase(SQLModel):
    pass

class Categories(CategoriesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category_name: str = Field(index=True)
    description: str | None = None
    created_at: str = Field(default="now")

class CategoriesCreate(CategoriesBase):
    category_name: str 
    description: str | None = None
    created_at: str | None = None

class CategoriesPublic(CategoriesBase):
    id: int 
    category_name: str
    description: str | None = None
    created_at: str

class CategoriesUpdate(CategoriesBase):
    id: int | None = None
    category_name: str | None = None
    description: str | None = None
    created_at: str | None = None

