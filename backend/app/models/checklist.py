"""
EOS - Checklist Model
Etkinliğe bağlı çeki listesi kalemlerini temsil eder.
QR durum döngüsü: Hazırlandı → Yüklendi → Kuruldu → Toplandı
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ChecklistItem(Base):
    __tablename__ = "checklist_items"

    id = Column(Integer, primary_key=True, index=True)
    etkinlik_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    envanter_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    adet = Column(Integer, nullable=False, default=1)

    # QR Durum Döngüsü: Hazırlandı → Yüklendi → Kuruldu → Toplandı
    durum = Column(String(50), default="Hazırlandı")

    # Zaman damgaları her durum geçişi için
    hazirlandi_zamani = Column(DateTime, nullable=True)
    yuklendi_zamani = Column(DateTime, nullable=True)
    kuruldu_zamani = Column(DateTime, nullable=True)
    toplandi_zamani = Column(DateTime, nullable=True)

    personel_notu = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    event = relationship("Event", back_populates="checklist_items")
    inventory_item = relationship("InventoryItem", back_populates="checklist_items")
