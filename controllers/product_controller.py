from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from models.products import Products
from schema.products_schema import ProductsCreate, ProductUpdate


# post product
async def post_product_controller(session: AsyncSession, product: ProductsCreate):
    db_product = Products.model_validate(product)
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product

# get all products
async def get_products_controller(session: AsyncSession):
    statement = select(Products)
    product = await session.exec(statement)
    product = product.all()
    return product

#get products by id
async def get_product_controller(session: AsyncSession, title: str):
    statement = select(Products).where(Products.title == title)
    result = await session.exec(statement)
    result = result.first()
    if not result:
        raise HTTPException(status_code=404, detail="product with the given id not found! ")
    return result

#delete products by id
async def delete_product_controller(session: AsyncSession, title: str):
    statement = select(Products).where(Products.title == title)
    result = await session.exec(statement)
    result = result.first()
    if not result:
        raise HTTPException(status_code=404, detail="product with given title not found! ")
    await session.delete(result)
    await session.commit()
    
    return {"message": "product deleted successfully!"}  # return a message to the clientl

#update product using title
def update_product_controller(session: AsyncSession, product: ProductUpdate):
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