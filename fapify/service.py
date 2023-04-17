#from fastapi import APIRouter, HTTPException, Query, Request
#from fastapi.responses import JSONResponse
#from typing import List
#from sqlalchemy.orm import Session, sessionmaker
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from fastapi_crudrouter import SQLAlchemyCRUDRouter

class Service():
    
    def __init__(self, model: object, db: object):
        self.tbl = model   
        self.primarykey = self.tbl.primary_key()
        self.db = db     
        self.name = model.__table__.name
        self.readschema = sqlalchemy_to_pydantic(self.tbl)
        self.writeschema = sqlalchemy_to_pydantic(self.tbl, exclude = [self.primarykey])
        self.writeschema.__name__ = self.name + "write"

        self.router = SQLAlchemyCRUDRouter(
            schema=self.readschema,
            create_schema=self.writeschema,
            db_model=self.tbl,
            db=self.db,
            prefix=self.name
        )
        
        
        #self.router = APIRouter()
        #self.router.add_api_route("/{}".format(self.name), self.getall, response_model=List[self.readschema], methods=["GET"], tags=[self.name])
        #self.router.add_api_route("/{}/".format(self.name)+"{"+self.tbl.primary_key()+"}", self.getone, response_model=self.readschema, methods=["GET"], tags=[self.name])
        #self.router.add_api_route("/{}/".format(self.name)+"{"+self.tbl.primary_key()+"}", self.deleteone, methods=["DELETE"], tags=[self.name])
        #self.router.add_api_route("/{}".format(self.name)+"{"+self.tbl.primary_key()+"}", self.createone, response_model=self.writeschema, methods=["PUT"], tags=[self.name])
        #self.router.add_api_route("/{}".format(self.name), self.createone, response_model=self.writeschema, methods=["POST"], tags=[self.name])
    
    '''
    def getall(self, offset: int = 0, limit: int = Query(default=100, lte=100)):
        with Session(bind = self.db) as session:
            records = session.query(self.tbl).offset(offset).limit(limit).all()
            return records
    
    def getone(self, id: int):
        with Session(bind = self.db) as session:
            record = session.get(self.tbl, id)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        return record
    
    
    def deleteone(self, id: int):
        with Session(bind = self.db) as session:
            record = session.get(self.tbl, id)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        else:
            session.delete(record)
            session.commit()
        return {"deleted": True}
    
    def createone(self, record: Request):
        with Session(bind = self.db) as session:
            session.add(record)
            session.commit()
            session.refresh(record)
            return record
   ''' 