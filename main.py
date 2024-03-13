from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi import Query
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/about")
def read_about():
    return {"About": "FastAPI"}

#path parameter
@app.get("/blog/{blog_id}")
def read_blog(blog_id: int): #int is the type of the parameter it is fixed
    return {"Blog ID": blog_id}

#query parameter
@app.get("/blog")
def read_blog(query: bool, limit: str= Query(min_length=3), published: Optional[bool] = False):
   if(published==True):
    return {"Query": query, "Limit": limit , "Published": published}
   else:
    return {"Query": query, "Limit": limit, "Published": published}
   
#path and query parameter
@app.get("/blog/{blog_id}/comments")
def read_blog(blog_id: int ,limit:int = 10): #int is the type of the parameter it is fixed
    return {"Blog ID": blog_id , "Limit": limit}

#request body
class Blog(BaseModel):
    id: int
    name: str
    description: str
    published: Optional[bool]

@app.post("/blog")
def create_blog(blog: Blog):
    return blog

@app.put("/blog/{blog_id}/update")
def update_blog(blog: Blog, blog_id: int):
    blog.id = blog_id
    return blog
