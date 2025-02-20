from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..dependency import get_session

from ..models.products import Products
from ..schema.products_schema import Productsbase, ProductsCreate, ProductsPublic, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post("/", response_model=ProductsPublic)
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

@router.get("/")
async def read_products(
    *,
    session: Session = Depends(get_session),
):
    product = session.exec(select(Products)).all()
    return product

@router.get("/{product_id}")
async def read_products(
    *,
    session: Session = Depends(get_session),
    product_id: int,
):
    db_product = session.get(Products, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="product with the given id not found! ")
    return db_product

@router.delete("/{product_id}")
async def delete_user(
    *,
    session: Session = Depends(get_session),
    product_id: int
):
    db_product = session.get(Products, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="product with given id not found! ")
    session.delete(db_product)
    session.commit()
    
    return {"message": "product deleted successfully!"}  # return a message to the client