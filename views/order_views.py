from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from  database import get_session

from models.orders import Orders
from schema.orders_schema import OrderBase, Ordercreate, OrderPublic, OrderUpdate

from controllers.order_controller import post_order_controller, get_orders_controller, get_order_controller, delete_order_controller, update_order_controller

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

 
@router.post("/", response_model=OrderPublic)
async def create_order(*, session: AsyncSession = Depends(get_session), order: Ordercreate,):
    db_order = Orders.model_validate(order)
    session.add(db_order)
    await session.commit()
    return {"message": "user created successfully!"}
    #return post_order_controller(session=session, order=order)

@router.get("/")    # need to be fixed
async def get_orders(*, session: AsyncSession = Depends(get_session),):
    result = await session.execute(select(Orders))
    result = result.scalars().all()
    return result
    #return get_orders_controller(session=session)

@router.get("/{order_id}")
async def get_order(*, session: AsyncSession = Depends(get_session), order_id: int,):
    db_order = await session.exec(select(Orders).where(Orders.id == order_id))
    return db_order.first()
    #return get_order_controller(session=session, order_id=order_id)

@router.delete("/{order_id}")
async def delete_user(*, session: AsyncSession = Depends(get_session), order_id: int):
    db_order = await session.execute(select(Orders).where(Orders.id == order_id))
    db_order = db_order.scalars().first()
    if not db_order:
        raise HTTPException(status_code=404, detail="user with given username not found!")
    await session.delete(db_order)
    await session.commit()
    return {"message": "user have been deleted succesfully!"}
    #return delete_order_controller(session=session, order_id=order_id)

@router.patch ("/")
async def update_order(*,session: AsyncSession = Depends(get_session), order: OrderUpdate):
    db_order = await session.execute(select(Orders).where(order.card_number == Orders.card_number))
    db_order = db_order.scalar()
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
    await session.commit()
    return {"massage": "success!"}
    #return update_order_controller(session=session, order=order)
