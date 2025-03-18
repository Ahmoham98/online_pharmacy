from sqlmodel import Session, select
from fastapi import HTTPException

from models.products import Products
from schema.products_schema import ProductsCreate, ProductUpdate


# post product
def post_product_controller(session: Session, product: ProductsCreate):
    db_product = Products.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

# get all products
def get_products_controller(session: Session):
    product = session.exec(select(Products)).all()
    return product

#get products by id
def get_product_controller(session: Session, product_id: int):
    db_product = session.get(Products, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="product with the given id not found! ")
    return db_product

#delete products by id
def delete_product_controller(session: Session, product_id):
    db_product = session.get(Products, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="product with given id not found! ")
    session.delete(db_product)
    session.commit()
    
    return {"message": "product deleted successfully!"}  # return a message to the clientl

#update product using title
def update_product_controller(session: Session, product: ProductUpdate):
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