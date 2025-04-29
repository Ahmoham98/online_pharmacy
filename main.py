from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from views import user_views, product_views, order_views, order_item_views, category_views

import uvicorn

from database import async_engine


from contextlib import asynccontextmanager


DEFAULT_EXPIRATION = 3600

description = """
## Users
You will be able to:

* **Create users**
* **Read users**
* **update users**
* **update users**

## products
You will be able to:
* **Create products**
* **Read products**
* **update products**
* **delete products**

## orders
You will be able to:
* **Create orders**
* **Read orders**
* **update orders**
* **delete orders**


## order_items
You will be able to:
* **Create order items**
* **read order items**
* **update order items**
* **delete order items**


## categories
You will be able to:
* **Create categories**
* **Read categories**
* **update categories**
* **delete categories**

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    #Load the database
    await create_db_tables()
    
    yield

    


app = FastAPI(
    title="Online Pharmacy API's",
    description=description,
    summary="Online Pharmacy: save time by getting requirements online...",
    version="0.0.7",
    openapi_tags=tags_metadata
)

# cors middleware for controlling data access via origin
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:80",
    "http://127.0.0.1:80",
    "http://localhost",
    "http://127.0.0.1",
    "htttp://localhost:8080",
    "htttp://127.0.0.1:8080",
    "http://localhost/user"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_views.router)
app.include_router(product_views.router)
app.include_router(order_views.router)
app.include_router(order_item_views.router)
app.include_router(category_views.router)

# create all the table models that we have in our metADATA
async def create_db_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await create_db_tables()

@app.get("/")
async def get_root():
    return {"message": "Welcome to online pharmacy root! "}

#Implementing round robin Algorithm load balancer
from itertools import cycle # Helps you to create infinite cycle (useful for round-robin algorithem)

from fastapi import Request
import httpx
import json

with open("load_balancer/servers.json") as f:
    servers = json.load(f)


# Implementing round-robin algorithm
class LoadBalancer ():
    def __init__(self, servers):
        self.servers = servers
        self.pool = cycle(server["url"] for server in servers)
    
    def round_robin(self):
        return next(self.pool)


load_balancer = LoadBalancer(servers=servers)

#proxy for handle request among servers
@app.get("/{path:path}")
@app.post("/{path:path}")
@app.put("/{path:path}")
@app.delete("/{path:path}")
@app.patch("/{path:path}")
async def proxy(request: Request, path: str):
    backend_url = load_balancer.round_robin()  #Select backend url based on round-robin algorithm
    url = f"{backend_url}/{path}"
    
    # For forwarding the request
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method, url, headers=request.headers.raw, data=await request.body()
        )
    
    return response.json()

#redis in-memory caching
"""
you need to create a database and connect it using Redis class from redis python library...

import redis
r = redis.Redis(host='localhost', port=6379, db=0)

r.set('name', "Ahmad")

if r.get("name"):
    print ("cache hit")
else:
    print ("cache miss")"""

#fastapi caching
"""
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# with on_event declaration:
redis = aioredis.from_url("reids://localhost", encoding="utf8", decode_responses=True)
FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache:")
    
cache declaration after endpoint declaration:
@cache(expire=60)

"""

# reids caching with aiocache
"""
from aiocache import Cache
from aiocache.serializers import JsonSerializer
from fastapi import FastAPI, Depends

app = FastAPI()
cache = Cache(Cache.MEMORY, serializer=JsonSerializer()) / # OR YOU CAN GO FOR: / cache = Cache.from_url("redis://localhost:6379/0", serializer=JsonSerializer)

async def get_cache():
    return cache

@app.get ("items/{items_id})
async def read_item(item_id: int, cache: Cache = Depends(get_cache)):
    cache_key = f"item_{item_id}"
    item = await cache.get(cache_key)
    if item is not None:
        return item
    # Assume get_item_from_db is a function to fetch item from the database
    item = await get_item_from_db(item_id)
    await cache.set(cache_key, item, ttl= 10 * 60)  #cache for 10 minutes
    return item
"""

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")