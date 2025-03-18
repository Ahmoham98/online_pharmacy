from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from dependency import get_session

from models.products import Products
from schema.products_schema import Productsbase, ProductsCreate, ProductsPublic, ProductUpdate

from controllers.product_controller import post_product_controller, get_products_controller, get_product_controller, delete_product_controller, update_product_controller

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

 
@router.post("/", response_model=ProductsPublic)
async def create_products(*, session: Session = Depends(get_session), product: ProductsCreate,):
    return post_product_controller(session, product)

@router.get("/")
async def read_products(*, session: Session = Depends(get_session),):
    return get_products_controller(session)

@router.get("/{product_id}")
async def read_products(*, session: Session = Depends(get_session), product_id: int,):
    return get_product_controller(session=session, product_id=product_id)

@router.delete("/{product_id}")
async def delete_product(*, session: Session = Depends(get_session), product_id: int):
    return delete_product_controller(session, product_id)

@router.patch ("/")
async def update_product(*, session: Session = Depends(get_session), product: ProductUpdate):
    return update_product_controller(session, product)