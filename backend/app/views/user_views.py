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