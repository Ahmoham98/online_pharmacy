#//////////////////// fastapi, sqlmodel and pydantic importations ////////////////////////
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
)

#//////////////////// Asyncsession ////////////////////////
from database import get_session

#//////////////////// Models and Schemas importations ////////////////////////
from schema.order_items_schema import (
    OrderItemsCreate,
    OrderItemsPublic,
    OrderItemsUpdate
)

#//////////////////// Controllers class importation ////////////////////////
from controllers.order_items_controller import OrderItemsController

#//////////////////// dependencies importation ////////////////////////
from dependency import get_current_active_superuser


router = APIRouter(
    prefix="/order_items",
    tags=["order_items"],
)

@router.post("/", response_model=OrderItemsPublic)
async def create_order(*, session: AsyncSession = Depends(get_session), order_item: OrderItemsCreate, username: str = Depends(get_current_active_superuser),):
    return await OrderItemsController(session=session).post_order_items_controller(order_item=order_item)

@router.get("/")
async def get_orders(*, session: AsyncSession = Depends(get_session), username: str = Depends(get_current_active_superuser),):
    return await OrderItemsController(session=session).get_order_items_controller()

@router.get("/{orderitems_id}")
async def get_order(*, session: AsyncSession = Depends(get_session), order_item_id: int, username: str = Depends(get_current_active_superuser),):
    return await OrderItemsController(session=session).get_order_item_controller(order_item_id=order_item_id)

@router.delete("/{orderitem_id}")
async def delete_user(*, session: AsyncSession = Depends(get_session), order_item_id: int, username: str = Depends(get_current_active_superuser),):
    return await OrderItemsController(session=session).delete_order_item_controller(order_item_id=order_item_id)

@router.patch ("/")
async def update_order_items(*, session: AsyncSession = Depends(get_session), order_items: OrderItemsUpdate, username: str = Depends(get_current_active_superuser),):
    return await OrderItemsController(session=session).update_order_item_controller(order_items=order_items)