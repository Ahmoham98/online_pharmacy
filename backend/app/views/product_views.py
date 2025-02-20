from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..dependency import get_session

from ..models.products import Products
from ..schema.products_schema import Productsbase, ProductsCreate, ProductsPublic, ProductUpdate

router = APIRouter()


@router.post("/products/", response_model=ProductsPublic)
async def create_products(
    *,
    session: Session = Depends(get_session),
    product: ProductsCreate,
):
    db_product = Products.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.get("/products/")
async def read_products(
    *,
    session: Session = Depends(get_session),
):
    product = session.exec(select(Products)).all()
    return product

@router.get("/products/{product_id}")
async def read_products(
    *,
    session: Session = Depends(get_session),
    product_id: int,
):
    db_product = session.get(Products, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="product with the given id not found! ")
    return db_product