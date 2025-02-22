from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..dependency import get_session

from ..models.categories import Categories
from ..schema.categories_schema import CategoriesBase, CategoriesCreate, CategoriesPublic, CategoriesUpdate

from ..controllers.category_controller import post_category_controller, get_categories_controller, get_category_controller, delete_category_cotroller, update_category_controller

router = APIRouter(
    prefix="/category",
    tags=["categories"],
)


@router.post("/", response_model=CategoriesPublic)
async def create_order(*, session: Session = Depends(get_session), category_item: CategoriesCreate,):
    return post_category_controller(session=session, category_item=category_item)

@router.get("/")
async def get_orders(*, session: Session = Depends(get_session),):
    return get_categories_controller(session=session)

@router.get("/{category_id}")
async def get_order(*, session: Session = Depends(get_session), category_id: int,):
    return get_category_controller(session=session, category_id=category_id)

@router.delete("/{category_id}")
async def delete_user(*, session: Session = Depends(get_session), category_id: int):
    return delete_category_cotroller(session=session, category_id=category_id)

@router.patch ("/")
async def update_category(*, session: Session = Depends(get_session), category: CategoriesUpdate):
    return update_category_controller(session=session, category=category)


