from fastapi import FastAPI
from app.apis.user import router as user_router
from app.apis.comments import router as comment_router
from app.database import async_engine

app = FastAPI()

app.include_router(user_router)
app.include_router(comment_router)

@app.on_event("shutdown")
async def shutdown_event():
    await async_engine.dispose()