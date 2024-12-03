from fastapi import FastAPI
from app.apis.user import router as user_router
from app.apis.comments import router as comment_router

app = FastAPI()

app.include_router(user_router)
app.include_router(comment_router)