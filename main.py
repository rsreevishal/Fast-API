from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

Base = declarative_base()
class Jobs(Base):
    __tablename__ = "software"
    title = Column(String)
    category = Column(String)
    company = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    description = Column(String)
    type = Column(String)
    id = Column(Integer,primary_key=True)
    applied = Column(Integer) 

    def __init__(self,title,cat,com,city,state,coun,desc,typ,id):
        self.title = title
        self.category = cat
        self.company = com
        self.city = city
        self.state = state
        self.country = coun
        self.description = desc
        self.type = typ
        self.id = id
        self.applied = 0
    
    def toDict(self):
        result = {
            "title": self.title,
            "category": self.category,
            "company": self.company,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "description": self.description,
            "type": self.type,
            "id": self.id,
            "applied": self.applied
        }
        return result

class Job(BaseModel):
    title:str
    category:str
    company:str
    city:str
    state:str
    country:str
    description:str
    type:str

engine = create_engine("sqlite:///jobs.db")

session = sessionmaker(bind=engine)()

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "This API will provide you to perform CURD operations on job database"}

@app.get('/jobs/')
async def getAll():
    result = []
    data = session.query(Jobs).all()
    for row in data:
        result.append(row.toDict())
    return result

@app.post('/jobs/')
async def post(job:Job):
    data = job.dict()
    n = len(session.query(Jobs).all())
    result = Jobs(data["title"],data["category"],data["company"],data["city"],data["state"],data["country"],data["description"],data["type"],n)
    session.add(result)
    session.commit()
    return {
        "Status":200,
        "message": "The job is successfully added"
    }



@app.get('/job/{id}')
async def get(id:int):
    data = session.query(Jobs).filter(Jobs.id == id)
    result = data[0].toDict()
    return result

@app.post('/job/{id}/apply/')
async def apply(id:int):
    try:
        data = session.query(Jobs).filter(Jobs.id == id)
        data[0].applied += 1
        session.commit()
        return {
            "Status":200,
            "message": "The requested job is successfully registered"
        }
    except:
        return {
            "Status": 404,
            "message": "The requested ID not exist or internal server error"
        }
    
@app.delete('/job/{id}')
async def delete(id:int):
    try:
        #engine.execution_options(autocommit=True).execute(text("DELETE FROM software where id = \"{id}\""))
        user = session.query(Jobs).filter(Jobs.id == id)
        session.delete(user[0])
        session.commit()
        return {
            "Status":200,
            "message": "The record successfully deleted"
        }
    except:
        return {
            "Status": 404,
            "message": "The requested ID not exist or internal server error"
        }
    