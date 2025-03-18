from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from database import engine
from dependency import get_session
from schema.users_schema import UsersBase, UsersCreate, UsersPublic, UsersUpdate, UserInDB
from models.users import Users

from controllers.user_controller import get_users_controller, post_user_controller , get_user_controller, delete_user_controller, update_user_controller
import bcrypt

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "f24bfbb639da735d4ebb1fbf5d442fa9c2269295b6d7a2502b998485e5f92746"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

"""get_user_auth
Args:
username (str): username to authenticate

Returns:
user_in_db: user object from database if authenticated

Description:
used to authenticate a user. It takes a username as an argument and returns the user
"""
def get_user_auth(
    username: str,
):
    with Session(engine) as session:
        user_in_db = session.exec(select(Users).where(Users.username == username)).first()
        if user_in_db:
            return user_in_db
        else:
            raise HTTPException(status_code=400, detail="user with the given username cannot be found in database...")

"""authenticate_user
Args:
username (str): username to authenticate
password (str): password to authenticate

Returns:
user (User): user object if authentication is successful

Description:
authenticate user with the given username and password
"""
def authenticate_user(username: str, password: str):
    db_user = get_user_auth(username)
    if not db_user:
        return False
    # cahnging password and hashed password strign object to pybyte for bcrypt.checkpw usage
    password = password.encode()
    hashed_password = db_user.hashed_password.encode()
    if not bcrypt.checkpw(password, hashed_password):
        return False
    return db_user

"""create_access_token
Args:
data (dict): data to be encoded in token // data dict type should be in jwt format for encoding and decoding process
expires_delta (timedelta): time after which token expires

Returns:
token (str): access token

Description:
create access token using pyjwt library
for pyjwt library:
    pip install pyjwt
"""
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

"""get_current_user
Args:
token (str): access token
Returns:
user (User): user object

Description:
get current user using access token
"""
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user_auth(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.get("/", response_model=list[UsersPublic])
async def get_users(*, session: Session = Depends(get_session)):
        return get_users_controller(session)

#Creating a post request endpoint to /users

@router.post("/", response_model=UsersPublic)
async def create_user(*, session: Session = Depends(get_session), user : UsersCreate):
    return post_user_controller(session, user)

#Creating get request endpoint with sending parameters to /users with /users/{id}

@router.get("/{usename}/")
async def get_user(*, session: Session = Depends(get_session), username: str):
    return get_user_controller(session, username)

@router.delete("/{username}")
async def delete_user(*, session: Session = Depends(get_session), username: str):
    return delete_user_controller(session, username )

@router.patch ("/")
async def update_user(*, session: Session = Depends(get_session), user: UsersUpdate):
    return update_user_controller(session, user)


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UsersPublic)
async def read_user_me(
    current_user: Annotated[Users, Depends(get_current_user)]
):
    return current_user



