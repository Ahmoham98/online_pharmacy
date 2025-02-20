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
async def delete_product(
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

@router.patch ("/")
async def update_product(
    *,
    session: Session = Depends(get_session),
    product: ProductUpdate
):
    
    db_product = session.exec(select(Products).where(product.title == Products.title)).one()
    if product.title is None:
        raise HTTPException(status_code=405, detail="title field required")
    elif product.title == "string":
        raise HTTPException(status_code=405, detail="title field required")
    else:
        db_product.title = product.title
    
    if product.description is not None:
        db_product.description = product.description
    
    if product.unit_price is not None:
        db_product.unit_price = product.unit_price
    
    if product.sale_price is not None:
        db_product.sale_price = product.sale_price
    
    if product.is_active is not None:
        db_product.is_active = product.is_active
    
    if product.status is not None:
        db_product.status = product.status
    
    if product.created_at is not None:
        db_product.created_at = product.created_at
    
    if product.updated_at is not None:
        db_product.updated_at = product.updated_at
    
    
    session.add(db_product)
    session.commit()
    return {"massage": "success!"}