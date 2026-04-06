from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
from dependencies import role_required

router = APIRouter(prefix="/records", tags=["Records"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_record(
    record: schemas.RecordCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required(["admin"]))
):
    new_record = models.Record(
        **record.dict(),
        user_id=user["user_id"]   # ✅ attach user
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record

@router.get("/")
def get_records(
    type: str = None,
    category: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(role_required(["admin", "analyst"]))
):
    query = db.query(models.Record)

    if type:
        query = query.filter(models.Record.type == type)

    if category:
        query = query.filter(models.Record.category == category)

    records = query.offset(skip).limit(limit).all()

    return records

@router.put("/{record_id}")
def update_record(
    record_id: int,
    record: schemas.RecordUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required(["admin"]))
):
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()

    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    # update fields dynamically
    for key, value in record.dict(exclude_unset=True).items():
        setattr(db_record, key, value)

    db.commit()
    db.refresh(db_record)

    return db_record


@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required(["admin"]))
):
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()

    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(db_record)
    db.commit()

    return {"message": "Record deleted"}