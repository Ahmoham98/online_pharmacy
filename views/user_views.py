#//////////////////// Typing, Date and time importations ////////////////////////
from typing import Annotated
from datetime import timedelta

#//////////////////// fastapi, sqlmodel and pydantic importations ////////////////////////
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

#//////////////////// Asyncsession ////////////////////////
from database import get_session

#//////////////////// Models and Schemas importations ////////////////////////
from models.users import Users
from schema.Authentication_Token_schema import Token
from schema.users_schema import (
    UsersCreate,
    UsersPublic,
    UsersUpdate,
)

#//////////////////// Controllers class importation ////////////////////////
from controllers.user_controller import UserController

#//////////////////// Redis and decoration importation ////////////////////////
import json
from functools import wraps
import redis
# asynchronous redis connection is not working when try using aiocache even with having the aiocache library installed 
# check for the requirements...
#from aiocache import Cache


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



ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



router = APIRouter(
    prefix="/users"
)


@router.get("/", response_model=list[UsersPublic], openapi_extra={"x-aperture-labs-portal": "blue"}, operation_id="users_getusers_userviews_getall")
async def get_users(*, session: AsyncSession = Depends(get_session)):
    """ 
        Handles get_all user requests and hand it over to the backend to get all the users 
    """
    result = await UserController(session=session).get_users_controller()
    return result

#Creating a post request endpoint to /users
@router.post("/", response_model=UsersPublic)
async def create_user(*, session: AsyncSession = Depends(get_session), user : UsersCreate):
    """
        Handles post user request and hand it over to the backend to create a new user with given data
    """
    result = await UserController(session=session).post_user_controller(user=user)
    return result

#Creating get request endpoint with sending parameters to /users with /users/{id}  done *_*
@router.get("/{username}/")
async def get_user(*, session: AsyncSession = Depends(get_session), username: str):
    """ 
        Handles get user requests with the given username and hand it over to the backend to get the user with the given username
    """
    result = await UserController(session=session).get_user_controller(username=username)
    return result

@router.delete("/{username}")
async def delete_user(*, session: AsyncSession = Depends(get_session), username: str):
    """
        Handles delete requests and hand it over to the backend to manage delete operation
    """
    result = await UserController(session=session).delete_user_controller(username=username)
    return result

@router.patch ("/")
async def update_user(*, session: AsyncSession = Depends(get_session), user: UsersUpdate):
    """
        Handles partial update and send it over to the backend to manage the update oparation
    """
    result = await UserController(session=session).update_user_controller(user=user)
    return result

from views.Auth import Authentication 

#unit testing passed
@router.post("/login")
async def login_for_access_token(
    *,
    session: AsyncSession = Depends(get_session),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await Authentication(session=session).authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await Authentication(session=session).create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

#unit testing passed
@router.get("/me", response_model=UsersPublic)
async def read_user_me(
    *, 
    session: AsyncSession = Depends(get_session),
    token: Annotated[Token, Query()] = None, #should be pass new async authenticate_user_with_jwt
    
):
    current_user = await Authentication(session=session).authenticate_user_with_jwt(token)
    return current_user









@router.get("/{some_test}")
async def get_authentication(
    *,
    session: AsyncSession = Depends(get_session),
    username: str,
):
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    result = await Authentication(session=session).create_access_token(data={"sub": username}, expires_delta=access_token_expire)
    return Token(access_token=result, token_type="bearer")

@router.get("/useraftertoken/{token_test}")
async def current_user_authentication(token: Token):
    result = await Authentication.authenticate_user_with_jwt(token=token)





#handling returning responses using fastapi
from fastapi.responses import JSONResponse
from fastapi import Body

#///////////////////////////// testing nedpoint response handling code section bellow ////////////////////////////////////////

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}

@router.put("/some_response/")
async def some_response_to_request(
    item_id: str,
    name: Annotated[str | None, Body()] = None,
    size: Annotated[int | None,  Body()] = None,
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)

