from fastapi import FastAPI
from sqlmodel import SQLModel
from .views import user_views, product_views, order_views, order_item_views, category_views

from .database import engine
from .models import users, products, orders, order_items, categories

app = FastAPI()

app.include_router(user_views.router)
app.include_router(product_views.router)
app.include_router(order_views.router)
app.include_router(order_item_views.router)
app.include_router(category_views.router)

def create_db_tables():
    SQLModel.metadata.create_all(bind=engine)

def main():
    create_db_tables()

@app.on_event("startup")
def on_startup():
    create_db_tables()


if __name__ == "__main__":
    main()
