from fastapi import FastAPI
from .views import user_views

app = FastAPI()

app.include_router(user_views)


def main():
    pass


if __name__ == "__main__":
    main()