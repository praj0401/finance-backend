from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import Optional
import re


# -------- USER --------
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str
    role: str

    # 🔐 Validate role
    @field_validator("role")
    def validate_role(cls, value):
        value = value.lower()
        if value not in ["admin", "analyst", "viewer"]:
            raise ValueError("Invalid role")
        return value

    # 🔐 Password strength validation
    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")

        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    role: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("role")
    def validate_role(cls, value):
        if value:
            value = value.lower()
            if value not in ["admin", "analyst", "viewer"]:
                raise ValueError("Invalid role")
        return value


# -------- RECORD --------
class RecordCreate(BaseModel):
    amount: float = Field(gt=0)  # must be > 0
    type: str
    category: str = Field(min_length=2, max_length=50)
    date: date
    notes: Optional[str] = Field(default=None, max_length=200)

    # 🔐 Validate type + normalize
    @field_validator("type")
    def validate_type(cls, value):
        value = value.lower()
        if value not in ["income", "expense"]:
            raise ValueError("type must be 'income' or 'expense'")
        return value

    # 📅 Prevent future dates
    @field_validator("date")
    def validate_date(cls, value):
        if value > date.today():
            raise ValueError("Date cannot be in the future")
        return value


class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[str] = None
    category: Optional[str] = Field(default=None, min_length=2, max_length=50)
    date: Optional[date] = None
    notes: Optional[str] = Field(default=None, max_length=200)

    @field_validator("type")
    def validate_type(cls, value):
        if value:
            value = value.lower()
            if value not in ["income", "expense"]:
                raise ValueError("type must be 'income' or 'expense'")
        return value

    @field_validator("date")
    def validate_date(cls, value):
        if value and value > date.today():
            raise ValueError("Date cannot be in the future")
        return value