from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, model, database, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# @router.post("/login", response_model=schemas.Token)
# def login(user_credentials: schemas.userlogin, db: Session = Depends(get_db)):

#     user = (
#         db.query(model.User).filter(model.User.email == user_credentials.email).first()
#     )

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
#         )

#     if not utils.verify(user_credentials.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
#         )
#     # create token

#     access_token = oauth2.create_access_token(data={"user_id": user.id})

#     return {"access_token": access_token, "token_type": "bearer"}



def verify_login(email: str, password: str, db: Session):

    user = (
        db.query(model.User).filter(model.User.email == email).first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    if not utils.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    # create token

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


#from json
@router.post("/login", response_model=schemas.Token, status_code=201)
def login(user_credentials: schemas.userlogin, db: Session = Depends(get_db)):

    return verify_login(user_credentials.email, user_credentials.password, db)

#from swagger
@router.post("/token", response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    return verify_login(user_credentials.username, user_credentials.password, db)



