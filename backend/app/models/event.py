"""
EOS - Event Model
Etkinlik (düğün/nişan/organizasyon) bilgilerini temsil eden SQLAlchemy modeli.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    etkinlik_adi = Column(String(300), nullable=False)
    musteri_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    tarih = Column(String(20), nullable=False)  # YYYY-MM-DD format
    mekan = Column(String(300), nullable=False)
    mekan_giris_saati = Column(String(10), nullable=True)  # HH:MM
    mekan_cikis_saati = Column(String(10), nullable=True)  # HH:MM
    etkinlik_turu = Column(String(100), default="Düğün")  # Düğün, Nişan, Sünnet, Kurumsal, Kokteyl
    durum = Column(String(50), default="Planlandı")  # Planlandı, Aktif, Tamamlandı, İptal
    sorumlu_firma = Column(String(100), nullable=False)  # La Vita Bella, Umut Aybar, Ortak
    ekip_sayisi = Column(Integer, nullable=True)
    misafir_sayisi = Column(Integer, nullable=True)
    notlar = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="events")
    checklist_items = relationship("ChecklistItem", back_populates="event", cascade="all, delete-orphan")
    finances = relationship("Finance", back_populates="event", cascade="all, delete-orphan")
