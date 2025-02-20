from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..dependency import get_session

from ..models.orders import Orders
from ..schema.orders_schema import OrderBase, Ordercreate, OrderPublic, OrderUpdate

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", response_model=OrderPublic)
async def create_order(
    *,
    session: Session = Depends(get_session),
    order: Ordercreate,
):
    db_order = Orders.model_validate(order)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.get("/")
async def get_orders(
    *,
    session: Session = Depends(get_session),
):
    orders = session.exec(select(Orders)).all()
    return orders

@router.get("/{order_id}")
async def get_order(
    *,
    session: Session = Depends(get_session),
    order_id: int,
):
    db_order = session.get(Orders, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="order with given id is not found! ")
    return db_order

@router.delete("/{order_id}")
async def delete_user(
    *,
    session: Session = Depends(get_session),
    order_id: int
):
    db_order = session.get(Orders, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="order with given id not found! ")
    session.delete(db_order)
    session.commit()
    
    return {"message": "order deleted successfully!"}  # return a message to the client

@router.patch ("/")
async def update_order(
    *,
    session: Session = Depends(get_session),
    order: OrderUpdate
):
    
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