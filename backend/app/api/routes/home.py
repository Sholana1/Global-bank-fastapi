from fastapi import APIRouter

router = APIRouter(prefix="/home")

@router.get("/")
def Home():
    return {"message": "Welcome to the GlobalGen AI Bank API!"}