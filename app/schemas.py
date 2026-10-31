from pydantic import BaseModel, AwareDatetime, EmailStr, ConfigDict

# USER SCHEMAS


class Create_user(BaseModel):
    email: EmailStr
    password: str


class user_created(BaseModel):
    id: int
    email: EmailStr
    created_at: AwareDatetime

    model_config = ConfigDict(from_attributes=True)


class userlogin(BaseModel):
    email: EmailStr
    password: str


# AUTHENTICATION SCHEMAS


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int


# POST SCHEMAS


class basePost(BaseModel):
    content: str
    title: str


class CreatePost(basePost):
    published: bool = True


class UpdatePost(basePost):
    published: bool


class Post(basePost):
    id: int
    published: bool
    created_at: AwareDatetime
    user_id: int
    owner: user_created

    model_config = ConfigDict(from_attributes=True)


# classvote
class PostOut(BaseModel):
    Post: Post
    votes: int


class Vote(BaseModel):
    vote: int
    post_id: int
