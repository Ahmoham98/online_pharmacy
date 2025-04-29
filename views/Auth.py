#//////////////////// Typing, Date and time importations ////////////////////////
from typing import Annotated
from datetime import (
    datetime,
    timedelta,
    timezone
)

#//////////////////// Fastapi, sqlmodels and pydantic importations ////////////////////////
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

#//////////////////// Models and schemas ////////////////////////
from models.users import Users
from schema.users_schema import UsersPublic
from schema.Authentication_Token_schema import TokenData, Token

#//////////////////// hashing ////////////////////////
import bcrypt

#//////////////////// jwt for encode and decode ////////////////////////
import jwt

# openssl rand -hex 32
SECRET_KEY = "f24bfbb639da735d4ebb1fbf5d442fa9c2269295b6d7a2502b998485e5f92746"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class Authentication:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    # GET user form db using username
    """get_user_from_db
        Args:
        username (str): username to authenticate

        Returns:
        result: user object from database if authenticated

        Description:
        used to get user from db using username
    """
    async def get_user_from_db(self, username: str):
        statement = select(Users).where(Users.username == username)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="... Username not found! ...")
        return result
    
    """authenticate_user
        Args:
        username (str): username to authenticate
        password (str): password to authenticate

        Returns:
        result: user object if authentication is successful

        Description:
        authenticate user from db using received username and password
    """
    async def authenticate_user(self, username: str, password: str):
        result = await self.get_user_from_db(username)
        if not result: 
            raise HTTPException(status_code=401, detail="... User not received from database!... ")
        password = password.encode()
        hashed_password = result.hashed_password.encode()
        if not bcrypt.checkpw(password, hashed_password):
            raise HTTPException(status_code=408, detail=" ...Password is not correct!... ")
        return result 
    
    """create_access_token
        Args:
        data (dict): data to be encoded in token // data dict type should be in jwt format for encoding and decoding process
        expires_delta (timedelta): time which token expires after

        Returns:
        token (str): access token, token Type

        Description:
        create access token using pyjwt library
        for pyjwt library:
            pip install pyjwt
    """
    async def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        for_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        for_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(for_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    """get_current_user
        Args:
        token (str): access token, token-type dictionary(bearer)
        Returns:
        user (User): user object if token is valid

        Description:
        get current user after checking access token
    """
    #Annotated[str, Depends(oauth2_scheme)]
    #token: Token
    async def authenticate_user_with_jwt(self, token: Annotated[str, Depends(oauth2_scheme)]) -> UsersPublic | None:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            if not payload:
                return payload
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=410, detail="... username has not been received1 ...")
            token_data = TokenData(username=username)
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=410, detail="... username has not been received2 ...")
        user = await self.get_user_from_db(username=token_data.username)
        if user is None:
            raise HTTPException(status_code=410, detail="... username has not been received3 ...")
        return user