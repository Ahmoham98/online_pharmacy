from sqlmodel import SQLModel, Field
from pydantic import EmailStr

# Orders model
class OrderBase(SQLModel):
    total_price: int
    card_number: int
    card_expiration_date: int
    email: EmailStr
    phone: int
    address: str
    coupon: str
    discount: int
    status: str
    created_at: str = Field(default="now")
    updated_at: str = Field(default="now")

# Orders Input model
class Ordercreate(OrderBase):
    email: EmailStr | None = "None"
    coupon: str | None = "None"
    discount: str | None = "None"

# Orders Output model
class OrderPublic(OrderBase):
    total_price: int
    email: EmailStr
    phone: int
    address: str
    status: str
    created_at: str = Field(default="now")

# Orders Update(Patch) model
class OrderUpdate(SQLModel):
    total_price: int | None = None
    card_number: int | None = None
    card_expiration_date: int | None = None
    email: EmailStr | None = None
    phone: int | None = None
    address: str | None = None
    coupon: str | None = None
    discount: int | None = None
    status: str | None = None
    created_at: str | None = Field(default="now")
