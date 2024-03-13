from pydantic import BaseModel
from typing import List, Union

class Blog(BaseModel):
    title: str
    body: str


class User(BaseModel):
    username: str
    email: str
    password: str

class ShowUser1(BaseModel):
    username: str
    email: str
    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    username: str
    email: str
    blogs: List[Blog] = []
    class Config():
        orm_mode = True


    
class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser1
    class Config():
        orm_mode = True        

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None        