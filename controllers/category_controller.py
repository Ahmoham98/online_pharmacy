from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from models.categories import Categories
from schema.categories_schema import CategoriesCreate, CategoriesUpdate


class CategoryController:
    def __init__(self, session):
        self.session = session
    
    async def post_category_controller(self, category_item: CategoriesCreate):
        db_category_item = Categories.model_validate(category_item)
        self.session.add(db_category_item)
        await self.session.commit()
        await self.session.refresh(db_category_item)
        return db_category_item
    
    async def get_categories_controller(session: AsyncSession):
        statement = select(Categories)
        result = await session.exec(statement)
        result = result.all()
        return result
    
    async def get_category_controller(session: AsyncSession, name: str):
        statement = select(Categories).where(Categories.name == name)
        result = await session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="category with given id is not found! ")
        return result
    
    async def delete_category_cotroller(session: AsyncSession, name: str):
        statement = select(Categories).where(Categories.name == name)
        result = await session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="category with given id is not found! ")
        if not result:
            raise HTTPException(status_code=404, detail="category with given id not found! ")
        await session.delete(result)
        await session.commit()
        
        return {"message": "category deleted successfully!"}  # return a message to the client
    
    async def update_category_controller(session: AsyncSession, category: CategoriesUpdate):
        statement = select(Categories).where(category.name == Categories.name)
        result = await session.exec(statement)
        result = result.one()
        
        if category.name is None:
            raise HTTPException(status_code=405, detail="name field required")
        elif category.name == "string":
            raise HTTPException(status_code=405, detail="name field required")
        else:
            result.name = category.name
        
        if category.description is not None:
            result.description = category.description
        
        if category.created_at is not None:
            result.created_at = category.created_at
        
        session.add(result)
        await session.commit()
        return {"massage": "success!"}

