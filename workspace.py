from fastapi import FastAPI, HTTPException,Depends, Header
from starlette.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from typing import List
from cachetools import TTLCache
from datetime import datetime

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create the cache
cache = TTLCache(maxsize=1000, ttl=300)  # 5 minutes TTL for cache


# Pydantic schemas
class User(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str

class Post(BaseModel):
    text: str

# SQLAlchemy models
class UserDB(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True)
    password = Column(String)

class PostDB(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True)
    text = Column(String)
    created_at = Column(String)

# Create the table
Base.metadata.create_all(bind=engine)



# Dependency to get the current session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Authentication function
def authenticate_user(email: str = Header(...), token: str = Header(...), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == email, UserDB.password == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or token")
    return user

# Endpoints
@app.get('/', response_class=HTMLResponse)
def homepage():
    return """<html><head><title>Html content</title></head><body><h1> The various End point of this webservice includes /login, /signup, /getPosts, /deletePost, /addPost </h1></body></html>"""

@app.post("/signup", response_model=Token)
async def signup(user: User, db: Session = Depends(get_db)):
    # Create a new user
    db_user = UserDB(**user.dict()) 
    db.add(db_user)
    db.commit()
    # Return token
    print('user is signed up')
    return {"access_token": db_user.email}

@app.post("/login", response_model=Token)
async def login(user: User, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(UserDB).filter(UserDB.email == user.email, UserDB.password == user.password).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Return token
    return {"access_token": db_user.email, "status":"Logged in Successfully"}

@app.post("/addPost", response_model=str)
async def add_post(post: Post, token: str = Header(...), db: Session = Depends(get_db)):
    # Authenticate user
    user = authenticate_user(token=token, db=db)

    # Validate payload size
    if len(post.text.encode()) > 1024 * 1024:  # 1 MB limit
        raise HTTPException(status_code=413, detail="Payload too large")

    # Save post in memory
    post_id = datetime.now().strftime("%Y%m%d%H%M%S")
    db_post = PostDB(id=post_id, text=post.text, created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.add(db_post)
    db.commit()

    # Return post ID
    return post_id

@app.get("/getPosts", response_model=List[Post])
async def get_posts(token: str = Header(...), db: Session = Depends(get_db)):
    # Authenticate user
    user = authenticate_user(token=token)

    # Check cache
    if token in cache:
        return cache[token]

    # Get user's posts
    posts = db.query(PostDB).filter(PostDB.email == user.email).all()

    # Cache posts
    cache[token] = posts
    return posts

@app.delete("/deletePost", response_model=str)
async def delete_post(post_id: str, token: str = Header(...), db: Session = Depends(get_db)):
    # Authenticate user
    user = authenticate_user(token=token)

    # Delete post
    db.query(PostDB).filter(PostDB.id == post_id, PostDB.email == user.email).delete()
    db.commit()

    return {"message": "Post deleted successfully"}
