from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from models.orders import Orders
from schema.orders_schema import Ordercreate, OrderUpdate

class OrderController:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def post_order_controller(self, order:Ordercreate):
        db_order = Orders.model_validate(order)
        self.session.add(db_order)
        await self.session.commit()
        await self.session.refresh(db_order)
        return db_order
    
    async def get_orders_controller(self):
        statement = select(Orders)
        result = await self.session.exc(statement)
        result = result.all()
        return result
    
    async def get_order_controller(self, order_id: int):
        statement = select(Orders).where(Orders.id == order_id)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="order with given id is not found! ")
        return result
    
    async def delete_order_controller(self, order_id: int):
        statement = select(Orders).where(Orders.id == order_id)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="order with given id not found! ")
        await self.session.delete(result)
        await self.session.commit()
        
        return {"message": "order deleted successfully!"}  # return a message to the client
    
    async def update_order_controller(self, order: OrderUpdate):
        statement = select(Orders).where(order.card_number == Orders.card_number)
        db_order = await self.session.exec(statement)
        db_order = db_order.one()
        if order.total_price is None:
            raise HTTPException(status_code=405, detail="total_price field required")
        elif order.total_price == 0:
            raise HTTPException(status_code=405, detail="total_price field required")
        else:
            db_order.total_price = order.total_price
        
        if order.card_number is not None:
            db_order.card_number = order.card_number
        
        if order.card_expiration_date is not None:
            db_order.card_expiration_date = order.card_expiration_date
        
        if order.email is not None:
            db_order.email = order.email
        
        if order.phone is not None:
            db_order.phone = order.phone
        
        if order.address is not None:
            db_order.address = order.address
        
        if order.coupon is not None:
            db_order.coupon = order.coupon
        
        if order.discount is not None:
            db_order.discount = order.discount
        
        if order.status is not None:
            db_order.status = order.status
        
        if order.created_at is not None:
            db_order.created_at = order.created_at
        
        self.session.add(db_order)
        await self.session.commit()
        return {"massage": "success!"}


