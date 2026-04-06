from fastapi import FastAPI
from database import Base, engine
from routers import users, records, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Backend API")

app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"message": "API is running"}