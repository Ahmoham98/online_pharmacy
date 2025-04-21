from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


from database import get_session

from models.categories import Categories
from schema.categories_schema import CategoriesBase, CategoriesCreate, CategoriesPublic, CategoriesUpdate

from controllers.category_controller import CategoryController
#from controllers.category_controller import post_category_controller, get_categories_controller, get_category_controller, delete_category_cotroller, update_category_controller

router = APIRouter(
    prefix="/category",
    tags=["categories"],
)


@router.post("/", response_model=CategoriesPublic)
async def create_order(*, session: AsyncSession = Depends(get_session), category_item: CategoriesCreate,):
    """db_category = Categories.model_validate(category_item)
    session.add(db_category)
    await session.commit()
    return {"message": "category added succesfully! "}"""
    return await CategoryController(session=session).post_category_controller(category_item=category_item)
 
@router.get("/")            # need to be fixed
async def get_orders(*, session: AsyncSession = Depends(get_session),):
    """db_categories = await session.execute(select(Categories)).scalars().all()
    return db_categories"""
    return await CategoryController(session=session).get_categories_controller()

@router.get("/{category_name}")
async def get_order(*, session: AsyncSession = Depends(get_session), name: str,):
    """db_category_item = await session.execute(select(Categories).where(Categories.name == name))
    if not db_category_item:
        raise HTTPException(status_code=406, detail="categoriy with the given name has not found! ")
    db_category_item = db_category_item.scalar()
    return db_category_item"""
    return await CategoryController(session=session).get_category_controller(name=name)

@router.delete("/{category_id}")
async def delete_user(*, session: AsyncSession = Depends(get_session), name: str):
    """db_category = await session.execute(select(Categories).where(Categories.name == name))
    db_category = db_category.scalars().first()
    if not db_category:
        raise HTTPException(status_code=404, detail="user with given username not found!")
    await session.delete(db_category)
    await session.commit()
    return {"message": "user have been deleted succesfully!"}"""
    return await CategoryController(session=session).delete_category_cotroller(name=name)

@router.patch ("/")
async def update_category(*, session: AsyncSession = Depends(get_session), category: CategoriesUpdate):
    """db_category = await session.execute(select(Categories).where(category.name == Categories.name))
    db_category = db_category.scalar()
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
    await session.commit()
    return {"massage": "success!"}"""
    return await CategoryController(session=session).update_category_controller(category=category)


