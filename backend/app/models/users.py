from sqlmodel import SQLModel, Field


class UsersBase(SQLModel):
    username: str
    password: str
    email: str
    phone: int
    first_name: str
    last_name: str
    address: str
    role: str
    created_at: str


# defining the tabel

class User(UsersBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

# user input model

class UserCreate(UsersBase):
    email: str | None = None
    phone: int | None = None
    address: str | None = None
    created_at: str = Field(default="now")

# user output model

class UserPublic(UsersBase):
    email: str | None = None
    phone: int | None = None

# user update(patch) model

class UserUpdate(SQLModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None
    phone: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    role: str | None = None
    created_at: str | None = None



