from typing import Optional
from uuid import UUID
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from fastapi import FastAPI


app = FastAPI()

#model
class UserBase(BaseModel):
    user_id = UUID
    email : EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=64) 

class User(UserBase):
    fisrt_name: str = Field(...,min_length = 1, max_length = 50)
    last_name: str = Field(...,min_length = 1, max_length = 50)
    birth_date: Optional[date] = Field(default=None)

class Tweet(BaseModel):
    Tweet_id : UUID = Field(...)
    content : str = Field(..., max_length=256, min_items=1)
    created_at : datetime = Field(..., default=datetime.now())
    updated_at : Optional[datetime] = Field(default=None)
    by : User = Field(...)


@app.get("/")
def home():
    return {"message" : "hola monda"}