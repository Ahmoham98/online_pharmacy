from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from ..models.products import Products

# Categories table

class Categories(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = None
    created_at: str = Field(default="now")

    products: list["Products"] = Relationship(back_populates="category")