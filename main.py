from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from fastapi import FastAPI


app = FastAPI()

#model
class User(BaseModel):
    user_id = UUID
    email : EmailStr = Field(...)
    

class Tweet(BaseModel):
    pass




@app.get("/")
def home():
    return {"message" : "hola monda"}