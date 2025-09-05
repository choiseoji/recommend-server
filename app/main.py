from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Book Recommend API")
app.include_router(router)