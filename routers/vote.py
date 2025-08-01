from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from FastAPI90 import schemas,database,models,oauth2
router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Votes,db :Session = Depends(database.get_db),current_user : int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    post_exist = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post does not exsit")
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = f"You have already liked the post")
        new_vote = models.Votes(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"sucessfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "sucessfully deleted vote"}






