from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from models.order_items import OrderItems
from schema.order_items_schema import OrderItemsCreate, OrderItemsUpdate


class OrderItemsController:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def post_order_items_controller(self, order_item: OrderItemsCreate):
        db_order_items = OrderItems.model_validate(order_item)
        self.session.add(db_order_items)
        await self.session.commit()
        await self.session.refresh(db_order_items)
        return db_order_items
    
    async def get_order_items_controller(self):
        order_items = await self.session.exec(select(OrderItems))
        order_items = order_items.all()
        return order_items
    
    async def get_order_item_controller(self, order_item_id: int):
        statement = select(OrderItems).where(OrderItems.id == order_item_id)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="order with given id is not found! ")
        return result
    
    async def delete_order_item_controller(self, order_item_id: int):
        statement = select(OrderItems).where(OrderItems.id == order_item_id)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="order with given id not found! ")
        await self.session.delete(result)
        await self.session.commit()
        
        return {"message": "order deleted successfully!"}  # return a message to the client
    
    async def update_order_item_controller(self, order_items: OrderItemsUpdate):
        statement = select(OrderItems).where(order_items.title == OrderItems.title)
        result = await self.session.exec(statement)
        db_order_items = result.first()
        
        if order_items.title is None:
            raise HTTPException(status_code=405, detail="title field required")
        elif order_items.title == "string":
            raise HTTPException(status_code=405, detail="title field required")
        else:
            db_order_items.title = order_items.title
        
        if order_items.description is not None:
            db_order_items.description = order_items.description
        
        if order_items.amount is not None:
            db_order_items.amount = order_items.amount
        
        if order_items.total_price is not None:
            db_order_items.total_price = order_items.total_price
        
        if order_items.created_at is not None:
            db_order_items.created_at = order_items.created_at
        
        if order_items.updated_at is not None:
            db_order_items.updated_at = order_items.updated_at
        
        
        self.session.add(db_order_items)
        await self.session.commit()
        return {"massage": "success!"}







#post order items
def post_order_items_controller(session: AsyncSession, order_item: OrderItemsCreate):
    db_order_items = OrderItems.model_validate(order_item)
    session.add(db_order_items)
    session.commit()
    session.refresh(db_order_items)
    return db_order_items

#get order items
def get_order_items_controller(session: AsyncSession):
    order_items = session.exec(select(OrderItems)).all()
    return order_items

#get order items by id
async def get_order_item_controller(session: AsyncSession, order_item_id: int):
    statement = select(OrderItems).where(OrderItems.id == order_item_id)
    result = await session.exec(statement)
    result = result.first()
    if not result:
        raise HTTPException(status_code=404, detail="order with given id is not found! ")
    return result

#delete order item by id
async def delete_order_item_controller(session: AsyncSession, order_item_id: int):
    statement = select(OrderItems).where(OrderItems.id == order_item_id)
    result = await session.exec(statement)
    result = result.first()
    if not result:
        raise HTTPException(status_code=404, detail="order with given id not found! ")
    await session.delete(result)
    await session.commit()
    
    return {"message": "order deleted successfully!"}  # return a message to the client

#update order item using title
def update_order_item_controller(session: AsyncSession, order_items: OrderItemsUpdate):
    db_order_items = session.exec(select(OrderItems).where(order_items.title == OrderItems.title)).one()
    
    if order_items.title is None:
        raise HTTPException(status_code=405, detail="title field required")
    elif order_items.title == "string":
        raise HTTPException(status_code=405, detail="title field required")
    else:
        db_order_items.title = order_items.title
    
    if order_items.description is not None:
        db_order_items.description = order_items.description

    if order_items.amount is not None:
        db_order_items.amount = order_items.amount
        
    if order_items.total_price is not None:
        db_order_items.total_price = order_items.total_price
    
    if order_items.created_at is not None:
        db_order_items.created_at = order_items.created_at
    
    if order_items.updated_at is not None:
        db_order_items.updated_at = order_items.updated_at
    
    
    session.add(db_order_items)
    session.commit()
    return {"massage": "success!"}