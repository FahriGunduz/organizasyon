"""Inventory Pydantic Schemas"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InventoryBase(BaseModel):
    adi: str
    kategori: str
    toplam_adet: int
    firma: str
    qr_kodu: str
    aciklama: Optional[str] = None
    birim_fiyat: Optional[float] = None
    resim_url: Optional[str] = None
    aktif: Optional[int] = 1


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    adi: Optional[str] = None
    kategori: Optional[str] = None
    toplam_adet: Optional[int] = None
    firma: Optional[str] = None
    aciklama: Optional[str] = None
    birim_fiyat: Optional[float] = None
    resim_url: Optional[str] = None
    aktif: Optional[int] = None


class InventoryAvailability(BaseModel):
    """Belirli bir tarih için envanter uygunluk bilgisi."""
    id: int
    adi: str
    toplam_adet: int
    rezerve_adet: int
    musait_adet: int
    musait_mi: bool


class InventoryResponse(InventoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
