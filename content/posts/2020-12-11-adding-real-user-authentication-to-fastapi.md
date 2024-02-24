---
title: Adding Database Backed User Authentication to FastAPI
date: 2020-12-11T14:10:58-08:00
description: "A tutorial for adding database backed authentication to FastAPI"
categories:
    - code
    - python
    - tutorial
---

In this tutorial we will learn how to add database backed user authentication to our FastAPI application. Later is the series we will implement registration, password recovery, and more.

<!--more-->

So you're excited about [FastAPI](https://fastapi.tiangolo.com) and you've been following the excellent documentation. At some point, you'll come to the section on security which sets you up with a login view, some utilities for hashing passwords and a dependency injected current user object.

It works great! The only problem is now you are left with a working application, but your user database consists of a hardcoded dictionary. Obviously, this will not do for a real application.

In this tutorial, we will replace our fake users database dictionary with a real database backed user table. In the next part, we'll add a registration endpoint so that people can sign up for accounts and login to your application.

## Starting where you left off

If you haven't already, go through the [FastAPI documentation on security](https://fastapi.tiangolo.com/tutorial/security/). We are going to pick up where it leaves off and you should be familiar with the concepts and code presented.

We should have an `app.py` that looks like this:

```python
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$dQD2AD2Y.Aa8F3IliHPfk.yNESW7FZe3RmeT38K661sg/vds404ga",  # swordfish
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

In case it's been a while or you are starting from scratch, the minimum packages required to run this demo are:

    pip install fastapi uvicorn passlib python-jose python-multipart bcrypt

And you can start the application with:

    uvicorn app:app --reload

Now head over to the shiny auto-generated swagger docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and try it out. You should be able to click the "Authorize" button and login with the username and password:

username: johndoe \
password: swordfish

Just as you would expect from our `fake_users_db`.

Our goal now is to preserve this functionality while replacing `fake_users_db` with a real database.

## Creating Gold with SqlAlchemy

For this example we are going to use SqlAlchemy ORM to interact with our database. There are a few ORMs out there, but SqlAlchemy is one of the more popular ones and just recently began supporting asynchronous io, so it's perfect for use with FastApi. Install it:

    pip install install sqlalchemy --pre

_note: you can drop --pre if 1.4 is out of beta, which it might be by the time you read this._

To avoid adding to our already cluttered `main.py` file, we're going to create a new module, `database.py` and set up SqlAlchemy there:

```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite3.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()


async def get_db():
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()
```

The first few statements define an engine (connection) to the database, as well as declaring an ORM model base for us to use (next step).

We also define a method to get a database session. This will be used in conjunction with FastAPI's dependency injection system in order to provide access to the database where and when it is need.

We will also declare our `User` model, which will represent a user in the database:

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite3.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()


async def get_db():
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)
```

This is a typical Sqlalchemy declarative model. We've kept the structure the same as the users in our `fake_users_db` so that the changes in the rest of the application can remain minimal.

Speaking of changes in the main application, let's get to the meat and potatoes. We will modify `app.py` with the following:

```python
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import database
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    disabled: bool

    class Config:
        orm_mode = True


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


@app.on_event("startup")
async def start_db():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(db: AsyncSession, username: str) -> database.User:
    result = await db.execute(select(database.User).filter_by(username=username))
    return result.scalars().first()


async def authenticate_user(db: AsyncSession, username: str, password: str) -> database.User:
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: AsyncSession = Depends(database.get_db), token: str = Depends(oauth2_scheme)) -> database.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> database.User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(db: AsyncSession = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

In the first changed block, we import a few things from Sqlalchemy that we will need, as well as import the database module we just defined.

We also modify the `User` Pydantic model. We want it to mirror the database representation so that it can correctly serialize data. Also notice the `orm_mode = True` line, that allows ORM objects (from sqlalchemy) to be passed in to Pydantic models (as we've defined here) and be correctly read and serialized.

At some point the database tables need to actually be created. A perfect time to do that would be when the app first starts up. So we use FastAPI's `startup` lifecycle hook to tell Sqlalchemy to create the tables we defined with the declarative base.

The rest of the changes are to `get_user(db: AsyncSession, username: str)` and simple modifications to the other methods that rely on it. Instead of doing a dictionary access in `fake_users_db` we do an actual query on our database to look up a user by their username.

Because `get_user` requires a database connection, we perform a dependency injection in `get_current_user` as well as `login_for_access_token`. This ensures the database session is available everywhere that we need it.

## Try it out

We now have a working application that functions pretty much the same as before, but will look up users in a Sqlite3 database instead of a dictionary. So how do we test it out? By inserting a user into the database of course!

First, make sure you are running your application. That will ensure the tables have been created (thanks to the `start_db` method we defined earlier).

    $ uvicorn app:app --reload

Next, let's add a user record to the generated `users` table.

From your command line, execute the following command:

    $ sqlite3 sqlite3.db

This will open up a sqlite3 shell. From here, we can use SQL to add a record to the `users` table:

```sql
INSERT INTO users VALUES (1, 'johndoe', 'johndoe@example.com', 'John Doe', false, '$2b$12$dQD2AD2Y.Aa8F3IliHPfk.yNESW7FZe3RmeT38K661sg/vds404ga');
```

Notice the big long string at the end: it's the same hashed password ("swordfish") that we hardcoded into `fake_users_db` before!

Once you've created the record, you should be able to go back to the [generated docs](127.0.0.1:8000/docs) and login as you did before. Now try out the `/users/me` endpoint, it will return the data we inserted into the database!

## Next steps

Manually adding users to your database is rarely what you want to do. In the next post in the series, we'll implement a registration view so that users can use your API to request accounts.
