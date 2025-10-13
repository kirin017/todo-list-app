from fastapi import FastAPI
from routers import todos, auth
from database.connection import engine, Base
from models import todo as todo_model
from models import user as user_model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")

# Include the todos router
app.include_router(todos.router)
app.include_router(auth.router)
@app.get("/")
def root():
    return {"message": "Welcome to Todo API"}

if __name__== "__main__":
    uvicorn.run(app, host="0.0.0.0.", port=8000)