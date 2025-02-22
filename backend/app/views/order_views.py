from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..dependency import get_session

from ..models.orders import Orders
from ..schema.orders_schema import OrderBase, Ordercreate, OrderPublic, OrderUpdate

from ..controllers.order_controller import post_order_controller, get_orders_controller, get_order_controller, delete_order_controller, update_order_controller

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", response_model=OrderPublic)
async def create_order(*, session: Session = Depends(get_session), order: Ordercreate,):
    return post_order_controller(session=session, order=order)

@router.get("/")
async def get_orders(*, session: Session = Depends(get_session),):
    return get_orders_controller(session=session)

@router.get("/{order_id}")
async def get_order(*, session: Session = Depends(get_session), order_id: int,):
    return get_order_controller(session=session, order_id=order_id)

@router.delete("/{order_id}")
async def delete_user(*, session: Session = Depends(get_session), order_id: int):
    return delete_order_controller(session=session, order_id=order_id)

@router.patch ("/")
async def update_order(*,session: Session = Depends(get_session), order: OrderUpdate):
    return update_order_controller(session=session, order=order)
