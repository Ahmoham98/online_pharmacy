from fastapi import FastAPI
from sqlmodel import SQLModel
from .views import user_views

from .database import engine
from .models import users, products, orders, order_items, categories

app = FastAPI()

app.include_router(user_views.router)


def create_db_tables():
    SQLModel.metadata.create_all(bind=engine)

def main():
    create_db_tables()


if __name__ == "__main__":
    main()