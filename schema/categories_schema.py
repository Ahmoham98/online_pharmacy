from sqlmodel import SQLModel

# Categories model
class CategoriesBase(SQLModel):
    name: str
    description: str | None = None
    created_at: str

# Categories Input model
class CategoriesCreate(CategoriesBase):
    created_at: str | None = "now"

# Categories Output models
class CategoriesPublic(CategoriesBase):
    id: int
    description: str | None = None

# Categories Update(Patch) model
class CategoriesUpdate(CategoriesBase):
    name: str | None = None
    description: str | None = None
    created_at: str | None = None

