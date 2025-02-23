from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..dependency import get_session

from ..models.order_items import OrderItems
from ..schema.order_items_schema import OrderItemsBase, OrderItemsCreate, OrderItemsPublic, OrderItemsUpdate

from ..controllers.order_items_controller import post_order_items_controller, get_order_items_controller, get_order_item_controller, delete_order_item_controller, update_order_item_controller

router = APIRouter(
    prefix="/order_items",
    tags=["order_items"],
)

 
@router.post("/", response_model=OrderItemsPublic)
async def create_order(*, session: Session = Depends(get_session), order_item: OrderItemsCreate,):
    return post_order_items_controller(session=session, order_item=order_item)

@router.get("/")
async def get_orders(*, session: Session = Depends(get_session),):
    return get_order_items_controller(session=session)

@router.get("/{orderitems_id}")
async def get_order(*, session: Session = Depends(get_session), order_item_id: int,):
    return get_order_item_controller(session=session, order_item_id=order_item_id)

@router.delete("/{orderitem_id}")
async def delete_user(*, session: Session = Depends(get_session), order_item_id: int):
    return delete_order_item_controller(session=session, order_item_id=order_item_id)

@router.patch ("/")
async def update_order_items(*, session: Session = Depends(get_session), order_items: OrderItemsUpdate):
    return update_order_item_controller(session=session, order_items=order_items)