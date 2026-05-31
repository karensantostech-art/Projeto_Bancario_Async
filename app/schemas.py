from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class TransactionBase(BaseModel):
    amount: float
    type: str


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    timestamp: datetime
    user_id: int


    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    balance: float

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

