from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from ..schema.users_schema import UsersUpdate, UsersCreate
from ..models.users import Users

from ..dependency import get_session 

# get all of the user
def get_users_controller( session: Session):
    users = session.exec(select(Users)).all()
    return users

# post user
def post_user_controller(session: Session, user: UsersCreate):
    db_user = Users.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# get user with id
def get_user_controller(session: Session, user_id: int):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found!")
    return db_user

# delete user with id
def delete_user_controller(session: Session, user_id):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user with given id not found! ")
    session.delete(db_user)
    session.commit()
    
    return {"message": "user deleted successfully!"}  # return a message to the client

# update user with username
def update_user_controller(session: Session, user: UsersUpdate):
    db_user = session.exec(select(Users).where(user.username == Users.username)).one()
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
    session.commit()
    return {"massage": "success!"}