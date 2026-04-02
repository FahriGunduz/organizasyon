"""
EOS - Status Engine Service
QR Kod Durum Döngüsü Yönetimi

Durum Döngüsü: Hazırlandı → Yüklendi → Kuruldu → Toplandı
İş Kuralı: Tüm kalemler 'Toplandı' olmadan etkinlik 'Tamamlandı' yapılamaz.
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.models.checklist import ChecklistItem
from app.models.inventory import InventoryItem
from app.models.event import Event


# QR Durum döngüsü sırası
STATUS_CYCLE = ["Hazırlandı", "Yüklendi", "Kuruldu", "Toplandı"]

STATUS_EMOJI = {
    "Hazırlandı": "📦",
    "Yüklendi": "🚛",
    "Kuruldu": "🎪",
    "Toplandı": "✅"
}


class StatusEngine:
    """QR kod tarama ve durum geçiş yönetimi servisi."""

    def __init__(self, db: Session):
        self.db = db

    def get_next_status(self, current_status: str) -> Optional[str]:
        """Bir sonraki durum adımını döndürür. Son adımda None döner."""
        try:
            idx = STATUS_CYCLE.index(current_status)
            if idx < len(STATUS_CYCLE) - 1:
                return STATUS_CYCLE[idx + 1]
            return None  # Zaten son aşamada (Toplandı)
        except ValueError:
            return STATUS_CYCLE[0]  # Bilinmeyen durumda ilk adıma döner

    def process_qr_scan(
        self,
        qr_kodu: str,
        etkinlik_id: int,
        personel_notu: Optional[str] = None
    ) -> dict:
        """
        QR kod taramasını işler ve durum geçişini gerçekleştirir.

        Args:
            qr_kodu: Taranan QR kod değeri
            etkinlik_id: İlgili etkinlik ID'si
            personel_notu: Saha personelinin notu (isteğe bağlı)

        Returns:
            dict: Tarama sonucu ve güncellenmiş durum bilgisi
        """
        # QR koda göre envanter kalemi bul
        inventory_item = self.db.query(InventoryItem).filter(
            InventoryItem.qr_kodu == qr_kodu
        ).first()

        if not inventory_item:
            return {
                'basarili': False,
                'mesaj': f'QR Kod bulunamadı: {qr_kodu}',
                'onceki_durum': None,
                'yeni_durum': None,
                'envanter_adi': None,
                'etkinlik_adi': None
            }

        # Etkinlik bilgisini al
        event = self.db.query(Event).filter(Event.id == etkinlik_id).first()
        if not event:
            return {
                'basarili': False,
                'mesaj': f'Etkinlik bulunamadı: ID {etkinlik_id}',
                'onceki_durum': None,
                'yeni_durum': None,
                'envanter_adi': inventory_item.adi,
                'etkinlik_adi': None
            }

        # Bu etkinlikteki çeki listesi kalemini bul
        checklist_item = self.db.query(ChecklistItem).filter(
            ChecklistItem.etkinlik_id == etkinlik_id,
            ChecklistItem.envanter_id == inventory_item.id
        ).first()

        if not checklist_item:
            return {
                'basarili': False,
                'mesaj': f'{inventory_item.adi} bu etkinliğin çeki listesinde değil',
                'onceki_durum': None,
                'yeni_durum': None,
                'envanter_adi': inventory_item.adi,
                'etkinlik_adi': event.etkinlik_adi
            }

        onceki_durum = checklist_item.durum
        yeni_durum = self.get_next_status(onceki_durum)

        if yeni_durum is None:
            return {
                'basarili': False,
                'mesaj': f'{inventory_item.adi} zaten son aşamada: {onceki_durum} ✅',
                'onceki_durum': onceki_durum,
                'yeni_durum': onceki_durum,
                'envanter_adi': inventory_item.adi,
                'etkinlik_adi': event.etkinlik_adi
            }

        # Durum güncelle ve zaman damgası ekle
        now = datetime.utcnow()
        checklist_item.durum = yeni_durum

        if yeni_durum == "Hazırlandı":
            checklist_item.hazirlandi_zamani = now
        elif yeni_durum == "Yüklendi":
            checklist_item.yuklendi_zamani = now
        elif yeni_durum == "Kuruldu":
            checklist_item.kuruldu_zamani = now
        elif yeni_durum == "Toplandı":
            checklist_item.toplandi_zamani = now

        if personel_notu:
            checklist_item.personel_notu = personel_notu

        self.db.commit()
        self.db.refresh(checklist_item)

        emoji = STATUS_EMOJI.get(yeni_durum, "")
        return {
            'basarili': True,
            'mesaj': f'{emoji} {inventory_item.adi}: {onceki_durum} → {yeni_durum}',
            'onceki_durum': onceki_durum,
            'yeni_durum': yeni_durum,
            'envanter_adi': inventory_item.adi,
            'etkinlik_adi': event.etkinlik_adi
        }

    def can_complete_event(self, etkinlik_id: int) -> dict:
        """
        Etkinliğin tamamlanıp tamamlanamayacağını kontrol eder.
        Tüm kalemler 'Toplandı' durumunda olmalı.
        """
        items = self.db.query(ChecklistItem).filter(
            ChecklistItem.etkinlik_id == etkinlik_id
        ).all()

        if not items:
            return {
                'tamamlanabilir': True,
                'toplam': 0,
                'toplandi': 0,
                'bekleyen': [],
                'mesaj': 'Çeki listesi boş'
            }

        toplandi = [i for i in items if i.durum == "Toplandı"]
        bekleyen = [i for i in items if i.durum != "Toplandı"]

        bekleyen_list = []
        for item in bekleyen:
            inv = self.db.query(InventoryItem).filter(
                InventoryItem.id == item.envanter_id
            ).first()
            if inv:
                bekleyen_list.append({
                    'adi': inv.adi,
                    'durum': item.durum,
                    'adet': item.adet
                })

        can_complete = len(bekleyen) == 0

        return {
            'tamamlanabilir': can_complete,
            'toplam': len(items),
            'toplandi': len(toplandi),
            'bekleyen': bekleyen_list,
            'mesaj': (
                'Tüm ekipmanlar toplandı, etkinlik tamamlanabilir ✅'
                if can_complete
                else f'{len(bekleyen)} kalem henüz "Toplandı" statüsünde değil'
            )
        }

    def get_event_progress(self, etkinlik_id: int) -> dict:
        """Etkinlik ekipman ilerleme özetini döndürür."""
        items = self.db.query(ChecklistItem).filter(
            ChecklistItem.etkinlik_id == etkinlik_id
        ).all()

        stats = {durum: 0 for durum in STATUS_CYCLE}
        for item in items:
            if item.durum in stats:
                stats[item.durum] += 1

        total = len(items)
        completed = stats.get("Toplandı", 0)

        return {
            'toplam': total,
            'durum_dagilimi': stats,
            'tamamlanma_yuzdesi': round((completed / total * 100) if total > 0 else 0, 1)
        }
