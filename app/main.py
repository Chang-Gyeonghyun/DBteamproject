from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.apis.user import router as user_router
from app.apis.comments import router as comment_router
from app.apis.post import router as post_router
from app.apis.like import router as like_router
from app.apis.follow import router as follow_router
from app.apis.attachment import router as attachment_router
from app.utils.exceptions import CustomException

app = FastAPI()

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

app.include_router(user_router)
app.include_router(comment_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(follow_router)
app.include_router(attachment_router)