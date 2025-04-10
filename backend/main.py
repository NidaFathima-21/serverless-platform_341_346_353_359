from fastapi import FastAPI
from api.routes import router as function_router

app = FastAPI()

# Mount function management router
app.include_router(function_router)
