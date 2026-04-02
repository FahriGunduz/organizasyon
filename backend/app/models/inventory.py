"""
EOS - Inventory Model
Ortak envanter havuzunu temsil eden SQLAlchemy modeli.
QR kod tabanlı takip için unique qr_kodu alanı içerir.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class InventoryItem(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    adi = Column(String(200), nullable=False)
    kategori = Column(String(100), nullable=False)  # Dekorasyon, Ses/Teknik, Mobilya, Aydınlatma, Tekstil, Diğer
    toplam_adet = Column(Integer, nullable=False, default=1)
    firma = Column(String(50), nullable=False)  # La Vita Bella, Umut Aybar, Ortak
    qr_kodu = Column(String(100), unique=True, index=True, nullable=False)
    aciklama = Column(String(500), nullable=True)
    birim_fiyat = Column(Float, nullable=True)
    resim_url = Column(String(500), nullable=True)
    aktif = Column(Integer, default=1)  # 1=aktif, 0=pasif
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    checklist_items = relationship("ChecklistItem", back_populates="inventory_item")
