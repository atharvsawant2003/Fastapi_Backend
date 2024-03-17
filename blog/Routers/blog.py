from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
import model, schemas,oauth2
from database import get_db

router = APIRouter(tags=["Blogs"])


@router.post("/create_blog",status_code=status.HTTP_201_CREATED)#tags are used to group the api
async def create_blog(request: schemas.Blog,db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    username = get_current_user.username
    user_id = db.query(model.User).filter(model.User.username == username).first().id
    new_blog = model.Blog(title=request.title, body=request.body, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/blogs",response_model=List[schemas.ShowBlog])
async def get_blogs(db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(model.Blog).all()
    return blogs

@router.get("/blogs/{id}",response_model=schemas.ShowBlog,status_code=200)
async def get_blog(id,db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
    
    return blog

@router.put("/update/{id}",status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    if not blog.first():
        return {"detail": "Blog not found"}
    blog.update(request.model_dump(),synchronize_session=False)
    db.commit()
    return {"detail": "Blog Updated"}

@router.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Blog Deleted"}