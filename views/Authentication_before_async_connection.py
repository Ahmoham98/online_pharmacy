#//////////////////// Typing, Date and time importations ////////////////////////
from typing import Annotated
from datetime import datetime, timedelta, timezone

#//////////////////// fastapi, sqlmodel and pydantic importations ////////////////////////
from fastapi import HTTPException, Depends, status
from sqlmodel import Session, select

#//////////////////// Models and schemas ////////////////////////
from models.users import Users
from schema.Authentication_Token_schema import Token, TokenData

#//////////////////// fastapi ////////////////////////
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordBearer

#//////////////////// jwt for encode and decode ////////////////////////
import jwt

#//////////////////// engine and Asyncengine ////////////////////////
from dependency import engine
from database import async_engine

#//////////////////// hashing ////////////////////////
import bcrypt


# openssl rand -hex 32
SECRET_KEY = "f24bfbb639da735d4ebb1fbf5d442fa9c2269295b6d7a2502b998485e5f92746"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#unit test passed
"""get_user_auth
Args:
username (str): username to authenticate

Returns:
user_in_db: user object from database if authenticated

Description:
used to authenticate a user. It takes a username as an argument and returns the user
"""
async def get_user_auth(
    session: AsyncSession,
    username: str,
):
    statement = select(Users).where(Users.username == username)
    result = await session.exec(statement)
    result = result.first()
    if not result:
        raise HTTPException(status_code=400, detail=" ...Username is not correct!...")
    
    return result

#unit test passed
"""authenticate_user
Args:
username (str): username to authenticate
password (str): password to authenticate

Returns:
user (User): user object if authentication is successful

Description:
authenticate user with the given username and password
"""
async def authenticate_user(username: str, password: str):
    db_user = await get_user_auth(username)
    if not db_user:
        raise HTTPException(status_code=408, detail="user not received from database! ")
    # changing password and hashed password string object to pybyte for bcrypt.checkpw usage
    password = password.encode()
    hashed_password = db_user.hashed_password.encode()
    if not bcrypt.checkpw(password, hashed_password):
        raise HTTPException(status_code=408, detail=" ...Password is not correct!... ")
    return db_user

# unit test passed
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
async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
#unit test passed
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
    user = await get_user_auth(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user



