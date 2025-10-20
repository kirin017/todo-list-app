from fastapi import FastAPI
from routers import todos, auth, categories
from database.connection import engine, Base
from models import todo as todo_model
from models import user as user_model
from models import category as category_model

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="A simple Todo API built with FastAPI",
    version="2.0.0")

# Include the todos router
app.include_router(todos.router)
app.include_router(auth.router)
app.include_router(categories.router)

@app.get("/")
def root():
    return {"message": "Welcome to Todo API",
            "features": [
                "User Authentication with JWT",
                "Create, Read, Update, Delete Todos",
                "Categorize Todos",
                "Filter and Sort Todos",
                "Overdue Todo Retrieval"
            ]
            }

if __name__== "__main__":
    uvicorn.run(app, host="0.0.0.0.", port=8000)