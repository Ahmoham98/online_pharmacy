from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..dependency import get_session

from ..models.categories import Categories
from ..schema.categories_schema import CategoriesBase, CategoriesCreate, CategoriesPublic, CategoriesUpdate

router = APIRouter(
    prefix="/category",
    tags=["categories"],
)


@router.post("/", response_model=CategoriesPublic)
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

@router.get("/")
async def get_orders(
    *,
    session: Session = Depends(get_session),
):
    db_category_items = session.exec(select(Categories)).all()
    return db_category_items

@router.get("/{category_id}")
async def get_order(
    *,
    session: Session = Depends(get_session),
    category_id: int,
):
    db_category = session.get(Categories, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="category with given id is not found! ")
    return db_category

@router.delete("/{category_id}")
async def delete_user(
    *,
    session: Session = Depends(get_session),
    category_id: int
):
    db_category = session.get(Categories, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="category with given id not found! ")
    session.delete(db_category)
    session.commit()
    
    return {"message": "category deleted successfully!"}  # return a message to the client

@router.patch ("/")
async def update_category(
    *,
    session: Session = Depends(get_session),
    category: CategoriesUpdate
):
    
    db_category = session.exec(select(Categories).where(category.name == Categories.name)).one()
    
    if category.name is None:
        raise HTTPException(status_code=405, detail="name field required")
    elif category.name == "string":
        raise HTTPException(status_code=405, detail="name field required")
    else:
        db_category.name = category.name
    
    if category.description is not None:
        db_category.description = category.description
    
    if category.created_at is not None:
        db_category.created_at = category.created_at
    
    
    session.add(db_category)
    session.commit()
    return {"massage": "success!"}


