from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..dependency import get_session

from ..models.categories import Categories
from ..schema.categories_schema import CategoriesBase, CategoriesCreate, CategoriesPublic, CategoriesUpdate

router = APIRouter()


@router.post("/category/", response_model=CategoriesPublic)
async def create_order(
    *,
    session: Session = Depends(get_session),
    category_item: CategoriesCreate,
):
    db_category_item = Categories.model_validate(category_item)
    session.add(db_category_item)
    session.commit()
    session.refresh(db_category_item)
    return db_category_item

@router.get("/category/")
async def get_orders(
    *,
    session: Session = Depends(get_session),
):
    db_category_items = session.exec(select(Categories)).all()
    return db_category_items

@router.get("/category/{category_id}")
async def get_order(
    *,
    session: Session = Depends(get_session),
    category_id: int,
):
    db_category = session.get(Categories, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="category with given id is not found! ")
    return db_category