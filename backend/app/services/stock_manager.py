"""
EOS - Stock Manager Service
Akıllı Rezervasyon Algoritması

İş Kuralı: Bir ekipman, aynı tarihteki iki farklı etkinliğe
toplam stok adedini aşacak şekilde rezerve edilemez.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.models.inventory import InventoryItem
from app.models.checklist import ChecklistItem
from app.models.event import Event


class StockManager:
    """Envanter çakışma kontrolü ve rezervasyon yönetimi servisi."""

    def __init__(self, db: Session):
        self.db = db

    def get_reserved_quantity(
        self,
        inventory_id: int,
        event_date: str,
        exclude_event_id: Optional[int] = None
    ) -> int:
        """
        Belirli bir tarihte bir envanter kalemi için toplam rezerve miktarını döndürür.
        Toplandı statüsündeki kalemler sayılmaz (geri depolara dönmüş).

        Args:
            inventory_id: Envanter kalemi ID'si
            event_date: YYYY-MM-DD formatında tarih
            exclude_event_id: Bu etkinliği hesaplamadan hariç tut (güncelleme için)
        """
        query = (
            self.db.query(func.sum(ChecklistItem.adet))
            .join(Event, Event.id == ChecklistItem.etkinlik_id)
            .filter(
                ChecklistItem.envanter_id == inventory_id,
                Event.tarih == event_date,
                ChecklistItem.durum != "Toplandı",
                Event.durum != "İptal"
            )
        )

        if exclude_event_id:
            query = query.filter(Event.id != exclude_event_id)

        result = query.scalar()
        return result or 0

    def get_available_quantity(
        self,
        inventory_id: int,
        event_date: str,
        exclude_event_id: Optional[int] = None
    ) -> int:
        """
        Belirli bir tarihte kullanılabilir envanter miktarını döndürür.
        """
        item = self.db.query(InventoryItem).filter(
            InventoryItem.id == inventory_id,
            InventoryItem.aktif == 1
        ).first()

        if not item:
            return 0

        reserved = self.get_reserved_quantity(inventory_id, event_date, exclude_event_id)
        return max(0, item.toplam_adet - reserved)

    def check_availability(
        self,
        inventory_id: int,
        event_date: str,
        requested_qty: int,
        exclude_event_id: Optional[int] = None
    ) -> dict:
        """
        Rezervasyon uygunluk kontrolü yapar.

        Returns:
            dict: {
                'musait': bool,
                'musait_adet': int,
                'rezerve_adet': int,
                'toplam_adet': int,
                'mesaj': str
            }
        """
        item = self.db.query(InventoryItem).filter(
            InventoryItem.id == inventory_id
        ).first()

        if not item:
            return {
                'musait': False,
                'musait_adet': 0,
                'rezerve_adet': 0,
                'toplam_adet': 0,
                'mesaj': 'Envanter kalemi bulunamadı'
            }

        reserved = self.get_reserved_quantity(inventory_id, event_date, exclude_event_id)
        available = max(0, item.toplam_adet - reserved)
        is_available = available >= requested_qty

        return {
            'musait': is_available,
            'musait_adet': available,
            'rezerve_adet': reserved,
            'toplam_adet': item.toplam_adet,
            'mesaj': (
                f'{item.adi}: {available} adet musait'
                if is_available
                else f'{item.adi}: Yetersiz stok! {available} musait, {requested_qty} talep edildi'
            )
        }

    def get_inventory_summary_for_date(self, event_date: str) -> list:
        """
        Belirli bir tarih için tüm envanterin uygunluk özetini döndürür.
        """
        items = self.db.query(InventoryItem).filter(InventoryItem.aktif == 1).all()
        summary = []

        for item in items:
            reserved = self.get_reserved_quantity(item.id, event_date)
            available = max(0, item.toplam_adet - reserved)
            summary.append({
                'id': item.id,
                'adi': item.adi,
                'kategori': item.kategori,
                'firma': item.firma,
                'toplam_adet': item.toplam_adet,
                'rezerve_adet': reserved,
                'musait_adet': available,
                'musait_mi': available > 0
            })

        return summary
