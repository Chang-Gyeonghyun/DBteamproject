from fastapi import FastAPI
from app.apis.user import router as user_router
from app.apis.comments import router as comment_router
from app.apis.post import router as post_router
from app.apis.like import router as like_router
from app.apis.follow import router as follow_router
from app.utils.middleware import RemoveEmptyFileMiddleware

app = FastAPI()
# app.add_middleware(RemoveEmptyFileMiddleware)

app.include_router(user_router)
app.include_router(comment_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(follow_router)