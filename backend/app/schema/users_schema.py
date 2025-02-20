from sqlmodel import SQLModel, Field

# Users model

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

#User Input model

class UsersCreate(UsersBase):
    email: str | None = None
    phone: int | None = None
    address: str | None = None
    created_at: str = Field(default="now")

# User Output model

class UsersPublic(UsersBase):
    id: int
    email: str | None = None
    phone: int | None = None

# User Update(Patch) model

class UsersUpdate(SQLModel):
    username: str 
    password: str | None = None
    email: str | None = None
    phone: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    role: str | None = None
    created_at: str | None = None


