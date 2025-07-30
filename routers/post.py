from typing import List, Optional
from sqlalchemy.orm import Session
from FastAPI90.database import get_db
from FastAPI90 import models,schemas,oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func

from FastAPI90.schemas import PostResponse

router = APIRouter(
    prefix="/posts",
    tags = ["posts"]
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user),limit : int = 10,skip : int = 0, search:Optional[str] = ""):
    posts = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).outerjoin(models.Votes,models.Votes.post_id == models.Post.id).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return [{"post": post, "votes": num_votes} for post, num_votes in posts]#when we do return posts_votes it returns a 500 Internal Error because we are trying to return a Tuple instead of json

@router.post("/", status_code= status.HTTP_201_CREATED ,response_model = schemas.PostResponse)#not working at all
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):#Post is a pydantic model which validates the data
        print(current_user.id)
        new_post = models.Post(**post.model_dump(),
                               owner_id = current_user.id)# better than doing post.title,post.comtent,post.published
        db.add(new_post)#adds to our database
        db.commit()#commits it
        db.refresh(new_post)# == Returning *
        return new_post


@router.get("/{id}",response_model = schemas.PostOut)
def get_post(id:int,db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
        query= db.query(models.Post,func.count(models.Votes.post_id).label("votes")).outerjoin(models.Votes,models.Votes.post_id == models.Post.id).group_by(models.Post.id).filter(models.Post.id == id)
        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist ")
        post_with_votes = query.first()
        if not post_with_votes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist ")
        post, votes = post_with_votes# post_with_votes == [post,votes] we just assigned post = post and votes = votes
        return {"post":post,"votes":votes}


@router.delete("/{id}")
def delete_post(id:int ,db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    #cursor.execute("""Delete from "Posts" where "Id" = %s returning *""",(str(id),))
    #post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Post with id:{id} does not exist ")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not Authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id:int, post:schemas.PostUpdate,db:Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_update = post_query.first()

    if post_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist ")
    if post_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not Authorized to perform requested action")

    post_query.update(post.model_dump(),synchronize_session = False)
    db.commit()
    return post_query.first()