from typing import Optional
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from fastapi import FastAPI, status


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
    content : str = Field(..., max_length=256, min_length=1)
    created_at : datetime = Field(default = None)
    updated_at : Optional[datetime] = Field(default=None)
    by : User = Field(...)



#path operations

##users

@app.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED, summary="Register a user", tags=["User"])
def signup():
    pass

@app.post("/login", response_model=User, status_code=status.HTTP_200_OK, summary="login a user", tags=["User"])
def login():
    pass

@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK, summary="show all user", tags=["User"])
def show_all_users():
    pass

@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, summary="show a user", tags=["User"])
def show_a_user():
    pass

@app.delete("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, summary="Delete a user", tags=["User"])
def delete_a_user():
    pass

@app.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, summary="Update a user", tags=["User"])
def update_a_user():
    pass


##tweets

@app.get("/", response_model=List[Tweet], status_code=status.HTTP_200_OK, summary="show all tweets", tags=["Tweets"])
def home():
    print("sapo hp")

@app.post("/post", response_model=Tweet, status_code=status.HTTP_201_CREATED, summary="Post a tweet", tags=["Tweets"])
def post():
    pass

@app.get("/tweets/{tweet_id}", response_model=Tweet, status_code=status.HTTP_200_OK, summary="show a tweet", tags=["Tweets"])
def show_a_tweet():
    pass


@app.delete("/tweets/{tweet_id}", response_model=Tweet, status_code=status.HTTP_200_OK, summary="delete a tweet", tags=["Tweets"])
def delete_a_tweet():
    pass


@app.put("/tweets/{tweet_id}", response_model=Tweet, status_code=status.HTTP_200_OK, summary="update a tweet", tags=["Tweets"])
def update_a_tweet():
    pass