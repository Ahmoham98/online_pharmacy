from sqlmodel import SQLModel, Field

# Categories table

class Categories(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = None
    category_name: str
    description: str | None = None
    created_at: str
    created_at: str = Field(default="now")
