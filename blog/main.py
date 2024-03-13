from fastapi import FastAPI
from model import Base
from database import SessionLocal, engine
from Routers import blog,user,authentication


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)

# @app.post("/create_user",status_code=status.HTTP_201_CREATED)
# async def create_user(request: schemas.User,db: Session = Depends(get_db)):
#     new_user = model.User(username=request.username, email=request.email, password=request.password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

#Encrypted Password

