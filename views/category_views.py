#//////////////////// fastapi, sqlmodel and pydantic importations ////////////////////////
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
)

#//////////////////// Asyncsession ////////////////////////
from database import get_session

#//////////////////// Models and Schemas importations ////////////////////////
from schema.categories_schema import (
    CategoriesCreate,
    CategoriesPublic,
    CategoriesUpdate
)

#//////////////////// Controllers class importation ////////////////////////
from controllers.category_controller import CategoryController

router = APIRouter(
    prefix="/category",
    tags=["categories"],
)


@router.post("/", response_model=CategoriesPublic)
async def create_order(*, session: AsyncSession = Depends(get_session), category_item: CategoriesCreate,):
    return await CategoryController(session=session).post_category_controller(category_item=category_item)

@router.get("/")            # need to be fixed
async def get_orders(*, session: AsyncSession = Depends(get_session),):
    return await CategoryController(session=session).get_categories_controller()

@router.get("/{category_name}")
async def get_order(*, session: AsyncSession = Depends(get_session), name: str,):
    return await CategoryController(session=session).get_category_controller(name=name)

@router.delete("/{category_id}")
async def delete_user(*, session: AsyncSession = Depends(get_session), name: str):
    return await CategoryController(session=session).delete_category_cotroller(name=name)

@router.patch ("/")
async def update_category(*, session: AsyncSession = Depends(get_session), category: CategoriesUpdate):
    return await CategoryController(session=session).update_category_controller(category=category)


