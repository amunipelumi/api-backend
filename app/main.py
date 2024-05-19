from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, user, post, vote
from .database import engine
# from . import models


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello! Welcome to the homepage..."}


### Notes
# Build out application 
# Check functionalities and output
# Define respective schemas, input and output
# Setup permissions and authorizations (tokens and security stuffs)
# Run multiple tests locally before deployment
###