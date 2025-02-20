from fastapi import FastAPI
from sqlmodel import SQLModel
from .views import user_views, product_views, order_views, order_item_views, category_views

from .database import engine
from .models import users, products, orders, order_items, categories

description = """
## Users
You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).

## products
You will be able to:
* **Create products** (_not implemented_).
* **Read products** (_not implemented_).

## orders
You will be able to:
* **Create orders** (_not implemented_).
* **Read orders** (_not implemented_).

## order_items
You will be able to:
* **Create order items** (_not implemented_).
* **read order items** (_not implemented_.)

## categories
You will be able to:
* **Create categories** (_not implemented_).
* **Read categories** (_not implemented_).

"""
tags_metadata = [
    {
        "name": "users",
        "description": "users endpoints. **login** Logic also implemented in here"
    },
    {
        "name": "products",
        "description": "products endpoints. **getting** & **reading** the products"
    },
    {
        "name": "orders",
        "description": "orders endpoints. **getting** & **reading** orders"
    },
    {
        "name": "order_items",
        "description": "order_items endpoints. **getting** & **reading** order_items"
    },
    {
        "name": "categories",
        "description": "categories endpoints. **getting** & **reading** categories"
    },
    {
        "name": "admin",
        "description": "admin part. for uploading and different accesses type from normal user"
    },
    {
        "name": "default",
        "description": "**get** root to check the server functionality and some other case usage"
    },
]

app = FastAPI(
    title="Online Pharmacy API's",
    description=description,
    summary="Online Pharmacy: save time by getting requirements online...",
    version="0.0.7",
    openapi_tags=tags_metadata
)

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
