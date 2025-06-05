from fastapi import FastAPI
from routes.todo import router as todo_router
from middlewares.logger import logging_middleware
from helpers.database import engine
from models.todo import Base

app = FastAPI(title="Todo API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(todo_router, prefix="/todos", tags=["todos"])

# Apply middleware
app.middleware("http")(logging_middleware)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)