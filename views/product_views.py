#//////////////////// fastapi, sqlmodel and pydantic importations ////////////////////////
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
)

#//////////////////// Asyncsession ////////////////////////
from database import get_session

#//////////////////// Models and Schemas importations ////////////////////////
from models.products import Products
from schema.products_schema import (
    Productsbase,
    ProductsCreate,
    ProductsPublic,
    ProductUpdate
)

#//////////////////// Controllers class importation ////////////////////////
from controllers.product_controller import ProductController

#//////////////////// dependencies importation ////////////////////////
from dependency import get_current_active_superuser

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

 
@router.post("/", response_model=ProductsPublic, deprecated=True)
async def create_products(*, session: AsyncSession = Depends(get_session), product: ProductsCreate, username: str = Depends(get_current_active_superuser),):
    return await ProductController(session=session).post_product_controller(product)

@router.get("/")
async def read_products(*, session: AsyncSession = Depends(get_session), username: str = Depends(get_current_active_superuser),):
    return await ProductController(session=session).get_products_controller() 

@router.get("/{product_title}")
async def read_products(*, session: AsyncSession = Depends(get_session), title: str, username: str = Depends(get_current_active_superuser),):
    return await ProductController(session=session).get_product_controller(title=title)

@router.delete("/{product_id}")
async def delete_product(*, session: AsyncSession = Depends(get_session), title: str, username: str = Depends(get_current_active_superuser),):
    return await ProductController(session=session).delete_product_controller(title=title)

@router.patch ("/")
async def update_product(*, session: AsyncSession = Depends(get_session), product: ProductUpdate, username: str = Depends(get_current_active_superuser),):
    return await ProductController(session=session).update_product_controller(product)