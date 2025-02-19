from sqlmodel import SQLModel, Field


class OrderBase(SQLModel):
    total_price: int
    card_number: int
    card_expiration_date: int
    email: str
    phone: int
    address: str
    coupon: str
    discount: int
    status: str
    created_at: str = Field(default="now")

class Orders(OrderBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    users_id: int | None = Field(default=None, foreign_key="users.id")

class Ordercreate(OrderBase):
    email: str | None = None
    coupon: str | None = None
    discount: str | None = None

class OrderPublic(OrderBase):
    total_price: int
    email: str
    phone: int
    address: str
    status: str
    created_at: str = Field(default="now")

class OrderUpdate(OrderBase):
    total_price: int | None = None
    card_number: int | None = None
    card_expiration_date: int | None = None
    email: str | None = None
    phone: int | None = None
    address: str | None = None
    coupon: str | None = None
    discount: int | None = None
    status: str | None = None
    created_at: str | None = Field(default="now")
