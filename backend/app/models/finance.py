"""
EOS - Finance Model
Etkinlik sözleşme ve ödeme takibi modeli.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Finance(Base):
    __tablename__ = "finances"

    id = Column(Integer, primary_key=True, index=True)
    etkinlik_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    toplam_tutar = Column(Float, nullable=False, default=0.0)
    kapora = Column(Float, default=0.0)
    kalan_odeme = Column(Float, default=0.0)
    odeme_tarihi = Column(String(20), nullable=True)  # YYYY-MM-DD
    sozlesme_tarihi = Column(String(20), nullable=True)  # YYYY-MM-DD
    durum = Column(String(50), default="Bekliyor")  # Bekliyor, Kısmi Ödeme, Tamamlandı
    odeme_yontemi = Column(String(100), nullable=True)  # Nakit, Havale, Kart
    fatura_no = Column(String(100), nullable=True)
    notlar = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    event = relationship("Event", back_populates="finances")
