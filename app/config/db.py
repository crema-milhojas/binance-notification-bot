import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

host = os.environ.get("POSTGRES_HOST")
port = os.environ.get("POSTGRES_PORT_INTERNAL")
user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
db_name = os.environ.get("POSTGRES_DB")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()