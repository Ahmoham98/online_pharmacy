from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException

from ..dependency import get_session
from ..schema.users_schema import UsersBase, UsersCreate, UsersPublic, UsersUpdate
from ..models.users import Users

router = APIRouter(
    prefix="/users",
    tags=["users"],)


#Creating get request for /users with a response model of defined User class that we can make python understand it using List from typing builtin python function
@router.get("/", response_model=list[UsersPublic])
async def get_users(
    *,
    session: Session = Depends(get_session),
):
        users = session.exec(select(Users)).all()
        return users

#Creating a post request endpoint to /users
@router.post("/", response_model=UsersPublic)
async def create_user(
    *,
    session: Session = Depends(get_session),
    user : UsersCreate
):
    db_user = Users.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

#Creating get request endpoint with sending parameters to /users with /users/{id}
@router.get("/{user_id}/")
async def get_user(
    *,
    session: Session = Depends(get_session),
    user_id: int
):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found!")
    return db_user

@router.delete("/{user_id}")
async def delete_user(
    *,
    session: Session = Depends(get_session),
    user_id: int
):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user with given id not found! ")
    session.delete(db_user)
    session.commit()
    
    return {"message": "user deleted successfully!"}  # return a message to the client

@router.patch ("/")
async def update_user(
    *,
    session: Session = Depends(get_session),
    user: UsersUpdate
):
    
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