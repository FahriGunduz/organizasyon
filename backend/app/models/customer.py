"""
EOS - Customer Model
Müşteri bilgilerini temsil eden SQLAlchemy modeli.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    tc_no = Column(String(11), unique=True, index=True, nullable=True)
    ad = Column(String(100), nullable=False)
    soyad = Column(String(100), nullable=False)
    telefon = Column(String(20), nullable=False)
    email = Column(String(200), nullable=True)
    adres = Column(String(500), nullable=True)
    firma_turu = Column(String(50), default="Bireysel")  # Bireysel, Kurumsal
    firma_adi = Column(String(200), nullable=True)
    notlar = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    events = relationship("Event", back_populates="customer")
