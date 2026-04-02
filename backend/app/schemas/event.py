"""Event Pydantic Schemas"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class EventBase(BaseModel):
    etkinlik_adi: str
    musteri_id: int
    tarih: str  # YYYY-MM-DD
    mekan: str
    mekan_giris_saati: Optional[str] = None
    mekan_cikis_saati: Optional[str] = None
    etkinlik_turu: Optional[str] = "Düğün"
    durum: Optional[str] = "Planlandı"
    sorumlu_firma: str
    ekip_sayisi: Optional[int] = None
    misafir_sayisi: Optional[int] = None
    notlar: Optional[str] = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    etkinlik_adi: Optional[str] = None
    musteri_id: Optional[int] = None
    tarih: Optional[str] = None
    mekan: Optional[str] = None
    mekan_giris_saati: Optional[str] = None
    mekan_cikis_saati: Optional[str] = None
    etkinlik_turu: Optional[str] = None
    durum: Optional[str] = None
    sorumlu_firma: Optional[str] = None
    ekip_sayisi: Optional[int] = None
    misafir_sayisi: Optional[int] = None
    notlar: Optional[str] = None


class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EventDetailResponse(EventResponse):
    """Ekipman ve finans bilgilerini de içeren detaylı etkinlik yanıtı."""
    musteri_adi: Optional[str] = None
    toplam_ekipman: int = 0
    tamamlanan_ekipman: int = 0
    ilerleme_yuzdesi: float = 0.0
