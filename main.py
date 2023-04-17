from fapify.app import AutomapModel, Service
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI


SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///db.sqlite3'

app = FastAPI()
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
AutomapModel.prepare(engine, reflect=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()


for tbl in AutomapModel.classes:    
    service = Service(tbl, get_db)    
    app.include_router(service.router)
