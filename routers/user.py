from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from FastAPI90 import utils, models, schemas
from FastAPI90.database import get_db

router = APIRouter(
    prefix="/users",
    tags = ["users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = f"{user.email} already has an account")

    #Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)  # adds to our database
    db.commit()  # commits it
    db.refresh(new_user)  # == Returning *
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id:int , db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"User with id:{id} does not exist")

    return user