from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..dependency import get_session

from ..models.order_items import OrderItems
from ..schema.order_items_schema import OrderItemsBase, OrderItemsCreate, OrderItemsPublic, OrderItemsUpdate

router = APIRouter(
    prefix="/order_items",
    tags=["order_items"],
)


@router.post("/", response_model=OrderItemsPublic)
async def create_order(
    *,
    session: Session = Depends(get_session),
    order_item: OrderItemsCreate,
):
    db_order_items = OrderItems.model_validate(order_item)
    session.add(db_order_items)
    session.commit()
    session.refresh(db_order_items)
    return db_order_items

@router.get("/")
async def get_orders(
    *,
    session: Session = Depends(get_session),
):
    order_items = session.exec(select(OrderItems)).all()
    return order_items

@router.get("/{orderitems_id}")
async def get_order(
    *,
    session: Session = Depends(get_session),
    order_items_id: int,
):
    order_items_id = session.get(OrderItems, order_items_id)
    if not order_items_id:
        raise HTTPException(status_code=404, detail="order_item with given id is not found! ")
    return order_items_id

@router.delete("/{orderitem_id}")
async def delete_user(
    *,
    session: Session = Depends(get_session),
    order_item_id: int
):
    db_order_item = session.get(OrderItems, order_item_id)
    if not db_order_item:
        raise HTTPException(status_code=404, detail="order_item with given id not found! ")
    session.delete(db_order_item)
    session.commit()
    
    return {"message": "order_item deleted successfully!"}  # return a message to the client

@router.patch ("/")
async def update_order_items(
    *,
    session: Session = Depends(get_session),
    order_items: OrderItemsUpdate
):
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