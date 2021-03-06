import json
from os import path, stat
from typing import Optional
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from fastapi import FastAPI, status, Body, HTTPException, Path
from pydantic.networks import HttpUrl


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


@app.post("/login", response_model=UserLogin, status_code=status.HTTP_200_OK, summary="login a user", tags=["User"])
def login(user: UserLogin = Body(...)):
    with open("users.json","r", encoding="utf-8") as f:
        esta = False
        users = json.loads(f.read())
        user_dict = user.dict()
        for i in users:
            if user_dict["email"] == i["email"] and user_dict["password"] == i["password"]:
                esta = True
        if esta:
            return user
        else:
            raise HTTPException(status_code=404, detail="user not found")

@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK, summary="show all user", tags=["User"])
def show_all_users():
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.loads(f.read())
        return users


@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, summary="show a user", tags=["User"])
def show_a_user(user_id: str = Path(...)):
     with open("users.json", "r", encoding="utf-8") as f:
        user = None
        users = json.loads(f.read())
        for i in users:
            if i["user_id"] == str(user_id):
                user = i
        if user is not None:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, summary="Delete a user", tags=["User"])
def delete_a_user(user_id: str = Path(...)):
    with open("users.json", "r+", encoding="utf-8") as f:
        found = False
        users = json.loads(f.read())
        for i in users:
            if i["user_id"] == str(user_id):
                found = True
                users.pop(users.index(i))
                f.seek(0)
                f.truncate()
                f.write(json.dumps(users))
        if not found:
            raise HTTPException(status_code=404, detail="user not exists")

@app.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, summary="Update a user", tags=["User"])
def update_a_user(user_id : str = Path(...), user: UserRegister = Body(...)):
    with open("users.json", "r+", encoding="utf-8") as f:
        found = False
        users = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        for i in users:
            if i["user_id"] == str(user_id):
                users[users.index(i)] = user_dict
                f.seek(0)
                f.truncate()
                f.write(json.dumps(users))
                found = True
        if not found:
            raise HTTPException(status_code=404, detail="user not exists")

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
def show_a_tweet(tweet_id : str = Path(...)):
    with open("tweets.json", "r", encoding="utf-8") as f :
        tw = None
        tweets = json.loads(f.read())
        for i in tweets:
            if i["Tweet_id"] == str(tweet_id):
                tw = i
        if tw is not None:
            return tw
        else:
            raise HTTPException(status_code=404, detail="tweet not found")

@app.delete("/tweets/{tweet_id}", response_model=Tweet, status_code=status.HTTP_200_OK, summary="delete a tweet", tags=["Tweets"])
def delete_a_tweet(tweet_id : str = Path(...)):
    with open("tweets.json", "r+", encoding="utf-8") as f :
        found = False
        tweets = json.loads(f.read())
        for i in tweets:
           if i["Tweet_id"] == str(tweet_id):
                found = True
                tweets.pop(tweets.index(i))
                f.seek(0)
                f.truncate()
                f.write(json.dumps(tweets))
        if not found:
            raise HTTPException(status_code=404, detail="tweet not found")

@app.put("/tweets/{tweet_id}", response_model=Tweet, status_code=status.HTTP_200_OK, summary="update a tweet", tags=["Tweets"])
def update_a_tweet(tweet_id: str = Path(...), tweet : Tweet = Body(...)):
    with open("tweets.json", "r+", encoding="utf-8") as f :
        found = False
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["Tweet_id"] = str(tweet_dict["Tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        for i in results:
            if i["Tweet_id"] == tweet_dict["Tweet_id"]:
                found = True
                results[results.index(i)] = tweet_dict
                f.seek(0)
                f.truncate()
                f.write(json.dumps(results))
        if found:
            return tweet_dict
        else:
            raise HTTPException(status_code=404, detail="tweet not exists")