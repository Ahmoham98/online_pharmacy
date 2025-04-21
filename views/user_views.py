#//////////////////// Typing, Date and time importations ////////////////////////
from typing import Annotated
from datetime import timedelta

#//////////////////// fastapi, sqlmodel and pydantic importations ////////////////////////
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

#//////////////////// Asyncsession ////////////////////////
from database import get_session

#//////////////////// Models and Schemas importations ////////////////////////
from schema.users_schema import UsersBase, UsersCreate, UsersPublic, UsersUpdate, UserInDB
from models.users import Users
from schema.Authentication_Token_schema import Token, TokenData

#//////////////////// Controllers class importation ////////////////////////
from controllers.user_controller import UserController


#//////////////////// authentication importation ////////////////////////
from views.Authentication import authenticate_user, create_access_token, get_current_user

#from controllers.user_controller import get_users_controller, post_user_controller , get_user_controller, delete_user_controller, update_user_controller

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

#unit testing passed
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

#unit testing passed
@router.get("/me", response_model=UsersPublic)
async def read_user_me(
    current_user: Annotated[Users, Depends(get_current_user)]
):
    return current_user



