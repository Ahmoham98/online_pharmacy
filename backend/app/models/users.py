from sqlmodel import SQLModel, Field

# defining the basemodel

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


# defining the table

class Users(UsersBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

# user input model

class UsersCreate(UsersBase):
    email: str | None = None
    phone: int | None = None
    address: str | None = None
    created_at: str = Field(default="now")

# user output model

class UsersPublic(UsersBase):
    id: int
    email: str | None = None
    phone: int | None = None

# user update(patch) model

class UsersUpdate(SQLModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None
    phone: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    role: str | None = None
    created_at: str | None = None



