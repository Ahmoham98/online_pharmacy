from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from models.orders import Orders
from schema.orders_schema import Ordercreate, OrderUpdate

#post order
def post_order_controller(session: AsyncSession, order:Ordercreate):
    db_order = Orders.model_validate(order)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

#get all orders
def get_orders_controller(session: AsyncSession):
    orders = session.exec(select(Orders)).all()
    return orders

#get order by id
def get_order_controller(session: AsyncSession, order_id: int):
    db_order = session.get(Orders, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="order with given id is not found! ")
    return db_order

#delete order by id
def delete_order_controller(session: AsyncSession, order_id: int):
    db_order = session.get(Orders, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="order with given id not found! ")
    session.delete(db_order)
    session.commit()
    
    return {"message": "order deleted successfully!"}  # return a message to the client

#update order with cardnumber
def update_order_controller(session: AsyncSession, order: OrderUpdate):
    db_order = session.exec(select(Orders).where(order.card_number == Orders.card_number)).one()

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
    
    session.add(db_order)
    session.commit()
    return {"massage": "success!"}
