from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
import model, schemas,hashing,oauth2
from database import get_db



router = APIRouter(tags=["Users"]) #prefix="/user"


@router.post("/create_user",status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.User,db: Session = Depends(get_db)):
   
    new_user = model.User(username=request.username, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users",response_model=List[schemas.ShowUser])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(model.User).all()
    return users

@router.get("/users/{id}",response_model=schemas.ShowUser,status_code=200)
async def get_user(id,db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id {id} is not available")
    user.blogs=db.query(model.Blog).filter(model.Blog.user_id == id).all()
    return user


@router.delete("/delete_user/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(model.User).filter(model.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id {id} is not available")
    user.delete(synchronize_session=False)
    db.commit()
    return {"detail": "User Deleted"}



