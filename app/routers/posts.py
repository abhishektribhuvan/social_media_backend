from fastapi import APIRouter
from typing import List
from random import randrange
from fastapi import HTTPException, Response, status, Depends
from .. import model, schemas, oauth2
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", tags=["posts"], dependencies=[Depends(oauth2.get_current_user)]
)


# Create_ Post
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """INSERT INTO social_posts(tital, content, published)
    #                 VALUES(%s, %s, %s) RETURNING *""",
    #     (post.tital, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = model.Post(title = post.title, content = post.content, published = post.published)//for less data abstraction
    new_post = model.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Get_All_Posts
@router.get(
    "/", response_model=List[schemas.PostOut], status_code=status.HTTP_202_ACCEPTED
)
# @router.get("/")
def all_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cursor.execute("""select * from social_posts""")
    # db_posts = cursor.fetchall()

    # db_posts = (
    #     db.query(model.Post)
    #     .filter(model.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    results = (
        db.query(model.Post, func.count(model.Votes.post_id).label("votes"))
        .join(model.Votes, model.Votes.post_id == model.Post.id, isouter=True)
        .group_by(model.Post.id)
        .filter(model.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return results


# Get_one_Post
@router.get(
    "/{id}", response_model=schemas.PostOut, status_code=status.HTTP_202_ACCEPTED
)
def show_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""select * from social_posts where id = %s""",(id))
    # post = cursor.fetchone()
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id :{id} is not found",
        )

    results = (
        db.query(model.Post, func.count(model.Votes.post_id).label("votes"))
        .join(model.Votes, model.Votes.post_id == model.Post.id, isouter=True)
        .group_by(model.Post.id)
        .filter(model.Post.id == id)
        .first()
    )
    print(results)
    return results


# Delete_post
@router.delete("/{id}", status_code=status.HTTP_205_RESET_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """DELETE FROM social_posts
    #                   WHERE id = %s returning*""",
    #     (id),
    # )
    # conn.commit()
    # delete_c = cursor.fetchone()
    post = db.query(model.Post).filter(model.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the id : {id} is not in the database",
        )

    if post.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post.delete()
    db.commit()

    return Response(status_code=status.HTTP_205_RESET_CONTENT)


# Update_Post
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(
    id: int,
    post: schemas.UpdatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """update social_posts set tital = %s, content = %s, published = %s where id = %s returning*""",
    #     (post.tital, post.content, post.published, id),
    # )
    # update_c = cursor.fetchone()
    # conn.commit()

    old_post = db.query(model.Post).filter(model.Post.id == id)

    if old_post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the id : {id} is not in the database",
        )

    if old_post.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    old_post.update(post.model_dump())
    # db.add(old_post)
    db.commit()
    # db.refresh(old_post)
    updated_post = db.query(model.Post).filter(model.Post.id == id)
    return updated_post.first()
