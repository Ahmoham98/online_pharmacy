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


router = APIRouter(
    prefix="/products",
    tags=["products"],
)

 
@router.post("/", response_model=ProductsPublic, deprecated=True)
async def create_products(*, session: AsyncSession = Depends(get_session), product: ProductsCreate,):
    return await ProductController(session=session).post_product_controller(product)

@router.get("/")
async def read_products(*, session: AsyncSession = Depends(get_session),):
    return await ProductController(session=session).get_products_controller() 

@router.get("/{product_title}")
async def read_products(*, session: AsyncSession = Depends(get_session), title: str,):
    return await ProductController(session=session).get_product_controller(title=title)

@router.delete("/{product_id}")
async def delete_product(*, session: AsyncSession = Depends(get_session), title: str):
    return await ProductController(session=session).delete_product_controller(title=title)

@router.patch ("/")
async def update_product(*, session: AsyncSession = Depends(get_session), product: ProductUpdate):
    return await ProductController(session=session).update_product_controller(product)