from sqlmodel import create_engine
from database import DATABASE_URL

engine = create_engine(DATABASE_URL)