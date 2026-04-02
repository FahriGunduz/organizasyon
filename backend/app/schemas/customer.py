"""Customer Pydantic Schemas"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    tc_no: Optional[str] = None
    ad: str
    soyad: str
    telefon: str
    email: Optional[str] = None
    adres: Optional[str] = None
    firma_turu: Optional[str] = "Bireysel"
    firma_adi: Optional[str] = None
    notlar: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    tc_no: Optional[str] = None
    ad: Optional[str] = None
    soyad: Optional[str] = None
    telefon: Optional[str] = None
    email: Optional[str] = None
    adres: Optional[str] = None
    firma_turu: Optional[str] = None
    firma_adi: Optional[str] = None
    notlar: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
