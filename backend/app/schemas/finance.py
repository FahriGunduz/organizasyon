"""Finance Pydantic Schemas"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FinanceBase(BaseModel):
    etkinlik_id: int
    toplam_tutar: float
    kapora: Optional[float] = 0.0
    kalan_odeme: Optional[float] = None
    odeme_tarihi: Optional[str] = None
    sozlesme_tarihi: Optional[str] = None
    durum: Optional[str] = "Bekliyor"
    odeme_yontemi: Optional[str] = None
    fatura_no: Optional[str] = None
    notlar: Optional[str] = None


class FinanceCreate(FinanceBase):
    pass


class FinanceUpdate(BaseModel):
    toplam_tutar: Optional[float] = None
    kapora: Optional[float] = None
    kalan_odeme: Optional[float] = None
    odeme_tarihi: Optional[str] = None
    sozlesme_tarihi: Optional[str] = None
    durum: Optional[str] = None
    odeme_yontemi: Optional[str] = None
    fatura_no: Optional[str] = None
    notlar: Optional[str] = None


class FinanceResponse(FinanceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    etkinlik_adi: Optional[str] = None

    class Config:
        from_attributes = True
