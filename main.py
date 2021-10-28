import json
from typing import Optional
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from fastapi import FastAPI, status, Body


app = FastAPI()

#model
class UserBase(BaseModel):
    user_id : UUID = Field(...)
    email : EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=64) 

class User(UserBase):
    fisrt_name: str = Field(...,min_length = 1, max_length = 50)
    last_name: str = Field(...,min_length = 1, max_length = 50)
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
    password: str = Field(..., min_length=8, max_length=64) 

class Tweet(BaseModel):
    Tweet_id : UUID = Field(...)
    content : str = Field(..., max_length=256, min_length=1)
    created_at : datetime = Field(default = None)
    updated_at : Optional[datetime] = Field(default=None)
    by : User = Field(...)



#path operations

##users

@app.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED, summary="Register a user", tags=["User"])
def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path register a user in the app

    Parameters:
        -request body parameter
            - user: UserRegister
    Return a json with basic information
        -user_id: UUID
        -email: EmailStr
        -first_name : str
        -last_name : str
        -birth_date : date
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user


@app.post("/login", response_model=User, status_code=status.HTTP_200_OK, summary="login a user", tags=["User"])
def login():
    pass

@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK, summary="show all user", tags=["User"])
def show_all_users():
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.loads(f.read())
        return users


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
    with open("tweets.json", "r", encoding="utf-8") as f:
        tweets = json.loads(f.read())
        return(tweets)

@app.post("/post", response_model=Tweet, status_code=status.HTTP_201_CREATED, summary="Post a tweet", tags=["Tweets"])
def post(tweet: Tweet = Body(...)):
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["Tweet_id"] = str(tweet_dict["Tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

@app.get("/tweets/{tweet_id}", response_model=Tweet, status_code=status.HTTP_200_OK, summary="show a tweet", tags=["Tweets"])
def show_a_tweet():
    pass


@app.delete("/tweets/{tweet_id}", response_model=Tweet, status_code=status.HTTP_200_OK, summary="delete a tweet", tags=["Tweets"])
def delete_a_tweet():
    pass


@app.put("/tweets/{tweet_id}", response_model=Tweet, status_code=status.HTTP_200_OK, summary="update a tweet", tags=["Tweets"])
def update_a_tweet():
    pass