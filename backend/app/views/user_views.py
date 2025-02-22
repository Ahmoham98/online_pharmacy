from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException

from ..dependency import get_session
from ..schema.users_schema import UsersBase, UsersCreate, UsersPublic, UsersUpdate
from ..models.users import Users

from ..controllers.user_controller import get_users_controller, post_user_controller , get_user_controller, delete_user_controller, update_user_controller

router = APIRouter(
    prefix="/users",
    tags=["users"],)


#Creating get request for /users with a response model of defined User class that we can make python understand it using List from typing builtin python function

@router.get("/", response_model=list[UsersPublic])
async def get_users(*, session: Session = Depends(get_session)):
        return get_users_controller(session)

#Creating a post request endpoint to /users

@router.post("/", response_model=UsersPublic)
async def create_user(*, session: Session = Depends(get_session), user : UsersCreate):
    return post_user_controller(session, user)

#Creating get request endpoint with sending parameters to /users with /users/{id}

@router.get("/{user_id}/")
async def get_user(*, session: Session = Depends(get_session), user_id: int):
    return get_user_controller(session, user_id)

@router.delete("/{user_id}")
async def delete_user(*, session: Session = Depends(get_session), user_id: int):
    return delete_user_controller(session, user_id)

@router.patch ("/")
async def update_user(*, session: Session = Depends(get_session), user: UsersUpdate):
    return update_user_controller(session, user)