from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from dependency import engine
from database import async_engine
from database import get_session
from schema.users_schema import UsersBase, UsersCreate, UsersPublic, UsersUpdate, UserInDB
from models.users import Users

#from controllers.user_controller import get_users_controller, post_user_controller , get_user_controller, delete_user_controller, update_user_controller
import bcrypt

import json
from functools import wraps
import redis
# asynchronous redis connection is not working when try using aiocache even with having the aiocache library installed 
# check for the requirements...
#from aiocache import Cache
from fastapi import HTTPException


# cache response decorator
def cache_response(ttl: int = 60, namespace: str = "main"):
    """caching decorator for fastapi endpoints

    Args:
        ttl (int, optional): Time to live for the cache in seconds. Defaults to 60.
        namespace (str, optional): Namespace for cache key in Redis. Defaults to "main".
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            username = kwargs.get('username') or args[0]  #I am assuming the user_id is the first argument
            cache_key = f"{namespace}:user:{username}"
            
            cache = redis.Redis(endpoint='localhost', port=6379, namespace=namespace)
            
            #Try to retrieve data from cache
            cached_value = await cache.get(cache_key)
            if cached_value :
                return json.loads(cached_value)
            
            #Call the actual function if cache is not hit\
            response = await func(*args, **kwargs)
            
            try:
                #Store the response in redis with a ttl
                await cache.set(cache_key, json.dumps(response), ttl=ttl)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error caching data: {e}")
            
            return response
        return wrapper
    return decorator


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
def get_user_auth(              # The session connection need to changed to asyncsession
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

from controllers.user_controller import UserController
@router.get("/", response_model=list[UsersPublic])
async def get_users(*, session: AsyncSession = Depends(get_session)):
    """ 
        Handles get_all user requests and hand it over to the backend to get all the users 
    """
    #return await get_users_controller(session)
    result = await UserController(session=session).get_users_controller()
    return result

#Creating a post request endpoint to /users
@router.post("/", response_model=UsersPublic)
async def create_user(*, session: AsyncSession = Depends(get_session), user : UsersCreate):
    """db_user = Users.model_validate(user)
    session.add(db_user)
    await session.commit() 
    return {"message": "user created successfully!"} """ # return a message to the client
    #return await post_user_controller(session, user)
    result = await UserController(session=session).post_user_controller(user=user)
    return result

#Creating get request endpoint with sending parameters to /users with /users/{id}  done *_*
# was working by adding redis decoration, some error from redis.__init__ happen, need to be check...
@router.get("/{username}/")
#@cache_response(ttl=120, namespace="users")
async def get_user(*, session: AsyncSession = Depends(get_session), username: str):
    """ 
        Handles get user requests with the given username and hand it over to the backend to get the user with the given username
    """
    #statement = select(Users).where(Users.username == username)
    #result = await session.exec(statement)
    #return result.first()
    
    
    #return await get_user_controller(session, username)
    
    result = await UserController(session=session).get_user_controller(username=username)
    return result

@router.delete("/{username}")
async def delete_user(*, session: AsyncSession = Depends(get_session), username: str):
    """
        Handles delete requests and hand it over to the backend to manage delete operation
    """
    #statement = select(Users).where(Users.username == username)
    #result = await session.exec(statement=statement)
    #result = result.first()
    #if not result:
    #    raise HTTPException(status_code=404, detail="user with given username not found!")
    #await session.delete(result)
    #await session.commit()
    #return {"message": "user have been deleted succesfully!"}"""
    
    
    #return await delete_user_controller(session, username )
    
    result = await UserController(session=session).delete_user_controller(username=username)
    return result

@router.patch ("/")
async def update_user(*, session: AsyncSession = Depends(get_session), user: UsersUpdate):
    """
        Handles partial update and send it over to the backend to manage the update oparation
    """
    """db_user = await session.execute(select(Users).where(user.username == Users.username))
    db_user = db_user.scalar()
    if user.username is None:
        raise HTTPException(status_code=405, detail="username field required")
    elif user.username == "string":
        raise HTTPException(status_code=405, detail="username field required")
    else:
        db_user.username = user.username
    
    #troubleshooting
    print(f"db_user username is {db_user.username}")
    print(f"db_user email address is {db_user.email}")
    print(f"db_user address is {db_user.address}")
    print(f"user input address is {user.address}")
    
    if user.password is not None:
        db_user.password = user.password
        
    if user.email is not None:
        db_user.email = user.email
    
    if user.phone is not None:
        db_user.phone = db_user.phone
    
    if user.first_name is not None:
        db_user.first_name = user.first_name
    
    if user.last_name is not None:
        db_user.last_name = user.last_name
    
    if user.address is not None:
        print ("address filed is not none ")
        db_user.address = user.address
    
    if user.role is not None:
        db_user.role = user.role
    
    if user.created_at is not None:
        db_user.created_at = user.created_at
    print (f"db_user is {db_user}")
    session.add(db_user)
    await session.commit()
    return {"massage": "success!"}"""
    #return await update_user_controller(session, user)
    
    result = await UserController(session=session).update_user_controller(user=user)
    return result

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



