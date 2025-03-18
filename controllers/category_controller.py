from sqlmodel import Session, select
from fastapi import HTTPException

from models.categories import Categories
from schema.categories_schema import CategoriesCreate, CategoriesUpdate


#post category
def post_category_controller(session: Session, category_item: CategoriesCreate):
    db_category_item = Categories.model_validate(category_item)
    session.add(db_category_item)
    session.commit()
    session.refresh(db_category_item)
    return db_category_item

#get categories
def get_categories_controller(session: Session):
    db_category_items = session.exec(select(Categories)).all()
    return db_category_items

#get category by id
def get_category_controller(session: Session, category_id: int):
    db_category = session.get(Categories, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="category with given id is not found! ")
    return db_category

#delete category by id
def delete_category_cotroller(session: Session, category_id: int):
    db_category = session.get(Categories, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="category with given id not found! ")
    session.delete(db_category)
    session.commit()
    
    return {"message": "category deleted successfully!"}  # return a message to the client

#update category with name of the category
def update_category_controller(session: Session, category: CategoriesUpdate):
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