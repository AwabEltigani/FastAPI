from fastapi import FastAPI, APIRouter
from FastAPI90 import models
from FastAPI90.database import engine
from routers import post, user ,authentication,vote
from FastAPI90.config import settings
from fastapi.middleware.cors import CORSMiddleware

#for the columns it doesnt pass the columns so we have to pass RealDictCursor


#models.Base.metadata.create_all(bind = engine) #creates table in pgadmin
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,#function that runs before every request
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],#specific http methods if not *
    allow_headers=["*"],
)
router = APIRouter()






app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my api"}










