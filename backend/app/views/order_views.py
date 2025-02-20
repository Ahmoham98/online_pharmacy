from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..dependency import get_session

from ..models.orders import Orders
from ..schema.orders_schema import OrderBase, Ordercreate, OrderPublic, OrderUpdate

router = APIRouter()


@router.post("/orders/", response_model=OrderPublic)
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

@router.get("/orders/")
async def get_orders(
    *,
    session: Session = Depends(get_session),
):
    orders = session.exec(select(Orders)).all()
    return orders

@router.get("/orders/{order_id}")
async def get_order(
    *,
    session: Session = Depends(get_session),
    order_id: int,
):
    db_order = session.get(Orders, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="order with given id is not found! ")
    return db_order