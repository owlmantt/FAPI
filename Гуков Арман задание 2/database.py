from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Используем правильный пароль для подключения
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Arman2007@localhost:5432/users_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"client_encoding": "utf8"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine) 