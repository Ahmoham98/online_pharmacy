from sqlmodel import Session, select
from fastapi import APIRouter, Depends

from ..dependency import get_session
from ..database import engine

from ..models.users import Users, UsersBase, UsersCreate, UsersPublic, UsersUpdate

router = APIRouter()


#Creating get request for /users with a response model of defined User class that we can make python understand it using List from typing builtin python function
@router.get("/users/", response_model=list[UsersPublic])
async def get_users(
    *,
    session: Session = Depends(get_session),
    user_id: int
):
        users = session.get(Users, user_id)
        return users

#Creating a post request endpoint to /users
@router.post("/users/", response_model=UsersPublic)
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
@router.get("/users/{user_id}/")
async def get_user(
    *,
    session: Session = Depends(get_session),
    user_id: int
):
    db_user = session.get(Users, user_id)
    return db_user