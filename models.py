from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # admin, analyst, viewer
    is_active = Column(Boolean, default=True)


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # income / expense
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))