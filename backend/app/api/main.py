from fastapi import APIRouter
from .routes import home

app_router = APIRouter()

app_router.include_router(home.router)