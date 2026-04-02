"""Checklist Pydantic Schemas"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChecklistItemBase(BaseModel):
    etkinlik_id: int
    envanter_id: int
    adet: int = 1
    durum: Optional[str] = "Hazırlandı"
    personel_notu: Optional[str] = None


class ChecklistItemCreate(ChecklistItemBase):
    pass


class ChecklistItemUpdate(BaseModel):
    adet: Optional[int] = None
    durum: Optional[str] = None
    personel_notu: Optional[str] = None


class ChecklistItemResponse(ChecklistItemBase):
    id: int
    hazirlandi_zamani: Optional[datetime] = None
    yuklendi_zamani: Optional[datetime] = None
    kuruldu_zamani: Optional[datetime] = None
    toplandi_zamani: Optional[datetime] = None
    created_at: datetime
    envanter_adi: Optional[str] = None

    class Config:
        from_attributes = True


class QRScanRequest(BaseModel):
    """QR kod tarama isteği."""
    qr_kodu: str
    etkinlik_id: int
    personel_notu: Optional[str] = None


class QRScanResponse(BaseModel):
    """QR kod tarama yanıtı."""
    basarili: bool
    mesaj: str
    onceki_durum: Optional[str] = None
    yeni_durum: Optional[str] = None
    envanter_adi: Optional[str] = None
    etkinlik_adi: Optional[str] = None
