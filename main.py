from fastapi import FastAPI
from database import Base, engine
from routers import users, records, dashboard

app = FastAPI(title="Finance Backend API")


# ✅ Create tables on startup (important for deployment)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# ✅ Include routers
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"message": "API is running"}