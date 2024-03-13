from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from Routers import blog,user
from database import get_db
import model, schemas,hashing
from datetime import timedelta
from jwttoken import ACCESS_TOKEN_EXPIRE_MINUTES,create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

@router.post("/login",status_code=status.HTTP_202_ACCEPTED)
async def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    #matching the password
    if not hashing.Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Incorrect Password")
    #creat
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}  
