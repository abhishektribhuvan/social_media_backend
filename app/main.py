from fastapi import FastAPI
from random import randrange
from . import model
from .database import engine
from .routers import posts, users, auth, votes
from pydantic_settings import BaseSettings
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

#model.Base.metadata.create_all(bind=engine)
#neeede when manually making the tables from alembic


app = FastAPI()
origins = ["*"]
# [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
#     "https://www.google.com"
# ]

#for all websites then just do ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],#specific methods allow
    allow_headers=["*"],#for specific head allow
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"messege": "Home page"}
