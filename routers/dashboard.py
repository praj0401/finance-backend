from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal
import models
from dependencies import role_required

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    user=Depends(role_required(["admin", "analyst", "viewer"]))
):
    income = db.query(func.sum(models.Record.amount)).filter(models.Record.type == "income").scalar() or 0
    expense = db.query(func.sum(models.Record.amount)).filter(models.Record.type == "expense").scalar() or 0

    return {
        "total_income": income,
        "total_expense": expense,
        "net_balance": income - expense
    }

@router.get("/category-summary")
def category_summary(
    db: Session = Depends(get_db),
    user=Depends(role_required(["admin", "analyst"]))
):
    results = (
        db.query(models.Record.category, func.sum(models.Record.amount))
        .group_by(models.Record.category)
        .all()
    )

    return [
        {"category": category, "total": total}
        for category, total in results
    ]

from sqlalchemy import extract

@router.get("/monthly-trends")
def monthly_trends(
    db: Session = Depends(get_db),
    user=Depends(role_required(["admin", "analyst"]))
):
    results = (
        db.query(
            extract('month', models.Record.date).label("month"),
            func.sum(models.Record.amount)
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

    return [
        {"month": int(month), "total": total}
        for month, total in results
    ]

@router.get("/recent")
def recent_activity(
    db: Session = Depends(get_db),
    user=Depends(role_required(["admin", "analyst", "viewer"]))
):
    records = (
        db.query(models.Record)
        .order_by(models.Record.date.desc())
        .limit(5)
        .all()
    )

    return records