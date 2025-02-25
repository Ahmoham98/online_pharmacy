from sqlmodel import SQLModel, Field
from pydantic import EmailStr
# Users model

class UsersBase(SQLModel):
    username: str
    email: EmailStr
    phone: int
    first_name: str
    last_name: str
    address: str
    role: str
    created_at: str

class UserInDB(UsersBase):
    hashed_password: str

#User Input model

class UsersCreate(UsersBase):
    email: EmailStr | None = None
    phone: int | None = None
    address: str | None = None
    created_at: str = Field(default="now")

# User Output model

class UsersPublic(UsersBase):
    id: int
    email: EmailStr | None = None
    phone: int | None = None

# User Update(Patch) model

class UsersUpdate(SQLModel):
    username: str 
    password: str | None = None
    email: EmailStr | None = None
    phone: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    role: str | None = None
    created_at: str | None = None


