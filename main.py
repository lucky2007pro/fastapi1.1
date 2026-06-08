from fastapi import FastAPI
import users.models
from database import engine
from users.routers import router as users_router

app = FastAPI()

users.models.Base.metadata.create_all(bind=engine)

app.include_router(users_router, prefix="/users", tags=["Users"])

@app.get("/")
def home():
    return {"message": "Dars 1 Home"}