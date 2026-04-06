from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas, auth

router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # 🔍 Check if email exists
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    # 🔐 Validate role FIRST
    if user.role not in ["admin", "analyst", "viewer"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    # 🔐 Hash password
    hashed_password = auth.hash_password(user.password)

    # 🧑‍💼 Create user
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }



@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = auth.create_access_token({
        "id": db_user.id,
        "role": db_user.role
    })

    return {"access_token": token}


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()