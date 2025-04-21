from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from database import get_session

from models.products import Products
from schema.products_schema import Productsbase, ProductsCreate, ProductsPublic, ProductUpdate

from controllers.product_controller import ProductController
#from controllers.product_controller import post_product_controller, get_products_controller, get_product_controller, delete_product_controller, update_product_controller

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

 
@router.post("/", response_model=ProductsPublic)
async def create_products(*, session: AsyncSession = Depends(get_session), product: ProductsCreate,):
    """db_product = Products.model_validate(product)
    session.add(db_product)
    await session.commit()
    return {"message": "user created successfully!"}"""
    return await ProductController(session=session).post_product_controller(session, product)

@router.get("/")
async def read_products(*, session: AsyncSession = Depends(get_session),):
    """statement = select(Products)
    result = await session.execute(statement=statement)
    return result.scalars()"""
    return await ProductController(session=session).get_products_controller(session) 

@router.get("/{product_title}")
async def read_products(*, session: AsyncSession = Depends(get_session), title: str,):
    """statement = select(Products).where(Products.id == product_id)
    result = await session.execute(statement=statement)
    return result.scalar_one()"""
    return await ProductController(session=session).get_product_controller(session=session, title=title)

@router.delete("/{product_id}")
async def delete_product(*, session: AsyncSession = Depends(get_session), title: str):
    """statement = select(Products).where(Products.id == product_id)
    result = await session.execute(statement=statement)
    result = result.scalar_one()
    
    await session.delete(result)
    await session.commit()
    
    return {"message": "user deleted successfully! "}"""
    return await ProductController(session=session).delete_product_controller(session, title=title)

@router.patch ("/")
async def update_product(*, session: AsyncSession = Depends(get_session), product: ProductUpdate):
    return await ProductController(session=session).update_product_controller(session, product)