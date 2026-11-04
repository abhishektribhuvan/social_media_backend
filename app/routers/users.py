from fastapi import APIRouter
from random import randrange
from fastapi import HTTPException, Response, status, Depends
from .. import model, schemas, utils
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/", response_model=schemas.user_created, status_code=status.HTTP_201_CREATED
)
async def create_user(user: schemas.Create_user, db: Session = Depends(get_db)):
    # password security
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = model.User(**user.model_dump())
    post = db.query(model.User).filter(model.User.email == new_user.email).first()
    if post:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user already exist")
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.user_created)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(model.User).filter(model.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id :{id} is not found",
        )

    return user
