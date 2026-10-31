from fastapi import APIRouter
from random import randrange
from fastapi import HTTPException, Response, status, Depends
from .. import model, schemas, utils, oauth2
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/")
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    check_vote = db.query(model.Votes).filter(
            model.Votes.post_id == vote.post_id, model.Votes.user_id == current_user.id
        )
    #post = db.query(model.Votes).filter(model.Votes.post_id == vote.post_id)

    if not check_vote.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist"
        )

    if vote.vote is 1:
        if check_vote.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        new_post = model.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return {"messege": "vote added successfully"}

    else:
        if not check_vote.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist"
            )
        check_vote.delete()
        db.commit()

        return {"messege": "successfully deleted the vote"}
