#//////////////////// fastapi, sqlmodel and pydantic importations ////////////////////////
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
)

#//////////////////// Asyncsession ////////////////////////
from  database import get_session

#//////////////////// Models and Schemas importations ////////////////////////
from schema.orders_schema import (
    Ordercreate,
    OrderPublic,
    OrderUpdate
)

#//////////////////// Controllers class importation ////////////////////////
from controllers.order_controller import OrderController

#//////////////////// dependencies importation ////////////////////////
from dependency import get_current_active_superuser

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@router.post("/", response_model=OrderPublic, deprecated=True)
async def create_order(*, session: AsyncSession = Depends(get_session), order: Ordercreate, username: str = Depends(get_current_active_superuser),):
    return await OrderController(session=session).post_order_controller(order=order)

@router.get("/")    # need to be fixed
async def get_orders(*, session: AsyncSession = Depends(get_session), username: str = Depends(get_current_active_superuser),):
    return await OrderController(session=session).get_orders_controller()

@router.get("/{order_id}")
async def get_order(*, session: AsyncSession = Depends(get_session), order_id: int, username: str = Depends(get_current_active_superuser),):
    return await OrderController(session=session).get_order_controller(order_id=order_id)

@router.delete("/{order_id}")
async def delete_user(*, session: AsyncSession = Depends(get_session), order_id: int, username: str = Depends(get_current_active_superuser),):
    return await OrderController(session=session).delete_order_controller(order_id=order_id)

@router.patch ("/")
async def update_order(*,session: AsyncSession = Depends(get_session), order: OrderUpdate, username: str = Depends(get_current_active_superuser),):
    return await OrderController(session=session).update_order_controller(order=order)
