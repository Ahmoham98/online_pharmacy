from sqlmodel import create_engine

DATABASE_URL = "postgresql://postgres:123456789@localhost:5432/online_pharmacy"
engine = create_engine(DATABASE_URL)