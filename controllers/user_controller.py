from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException
from schema.users_schema import UsersUpdate, UsersCreate
from models.users import Users
import bcrypt

from database import get_session

#Password hasher
async def get_password_hash(password):
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())

class UserController:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    # GET Functionalities
    async def get_users_controller(self):
        statement = select(Users)
        result = await self.session.exec(statement)
        result = result.all()
        if not result:
            raise HTTPException(status_code=404, detail="No users found! ")
        return result
    
    async def get_user_controller(self, username: str):
        statement = select(Users).where(Users.username == username)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="User with given username not found!... ")
        return result
    
    
    #POST Functionalities
    async def post_user_controller(self, user: UsersCreate):
        hashed_password = await get_password_hash(user.password)
        extra_data = {"hashed_password": hashed_password}
        db_user = Users.model_validate(user, update=extra_data)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user
    
    # DELETE Functionalities
    async def delete_user_controller(self, username: str):
        statement = select(Users).where(Users.username == username)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="User with given username not found! ")
        await self.session.delete(result)
        await self.session.commit()
        
        return {"message": "user has been deleted successfully!"}
    
    #UPDATE Functionalities
    async def update_user_controller(self, user: UsersUpdate):
        db_user = await self.session.exec(select(Users).where(user.username == Users.username))
        db_user = db_user.one()
        if user.username is None:
            raise HTTPException(status_code=405, detail="username field required")
        elif user.username == "string":
            raise HTTPException(status_code=405, detail="username field required")
        else:
            db_user.username = user.username
        
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
            db_user.address = user.address
        
        if user.role is not None:
            db_user.role = user.role
        
        if user.created_at is not None:
            db_user.created_at = user.created_at
        
        self.session.add(db_user)
        await self.session.commit()
        return {"massage": "success!"}



























async def get_password_hash(password):
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())

# get all of the user
async def get_users_controller(session: AsyncSession):
    users = await session.exec(select(Users))
    users = users.all()
    return users

# post user
async def post_user_controller(session: AsyncSession, user: UsersCreate):
    hashed_password = await get_password_hash(user.password)
    extra_data = {"hashed_password": hashed_password}
    db_user = Users.model_validate(user, update=extra_data)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

# Implementing monitoring and logging for continuous optimization
"""import time 

from contextlib import contextmanager

# Implementing monitoring and logging

@contextmanager
def query_performance_log():
    start_time = time.time()
    yield
    duration = time.time() - start_time
    logger.info(f"Query executed in {duration:.4f} seconds")

async def get_users():
    with query_performance_log():
        return await db.fetch_all("SELECT * FROM users")"""

# get user with id
async def get_user_controller(session: AsyncSession, username: int):
    statement = select(Users).where(Users.username == username)
    result = await session.exec(statement)
    if not result:
        raise HTTPException(status_code=404, detail="user with the given username have not been found... ")
    result = result.first()
    return result
    """db_user = await session.exec(select(Users).where(Users.username == username))
    db_user = db_user.first()
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found!")
    return db_user
"""

# delete user with id
async def delete_user_controller(session: AsyncSession, username):
    db_user = await session.exec(select(Users).where(Users.username == username))
    db_user = db_user.first()
    if not db_user:
        raise HTTPException(status_code=404, detail="user with the given username have not been found...  ")
    await session.delete(db_user)
    await session.commit()
    
    return {"message": "user deleted successfully!"}  # return a message to the client

# update user with username
async def update_user_controller(session: AsyncSession, user: UsersUpdate):
    db_user = await session.exec(select(Users).where(user.username == Users.username))
    db_user = db_user.one()
    if user.username is None:
        raise HTTPException(status_code=405, detail="username field required")
    elif user.username == "string":
        raise HTTPException(status_code=405, detail="username field required")
    else:
        db_user.username = user.username
    
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
        db_user.address = user.address
    
    if user.role is not None:
        db_user.role = user.role
    
    if user.created_at is not None:
        db_user.created_at = user.created_at
    
    session.add(db_user)
    await session.commit()
    return {"massage": "success!"}




