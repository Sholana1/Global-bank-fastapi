from fastapi import FastAPI

app = FastAPI(
    title="GlobalGen AI Bank API",
    description="API for GlobalGen AI Bank services",
)

@app.get("/")
def Home():
    return {"message": "Welcome to the GlobalGen AI Bank API!"}