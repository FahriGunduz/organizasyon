"""
EOS - QR Tracking API
QR tarama işlemleri ve saha onay endpoint'leri.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.status_engine import StatusEngine
from app.services.stock_manager import StockManager
from app.schemas.checklist import QRScanRequest, QRScanResponse
from app.models.checklist import ChecklistItem
from app.models.inventory import InventoryItem
from app.models.event import Event
from app.schemas.checklist import ChecklistItemCreate, ChecklistItemResponse, ChecklistItemUpdate
from typing import List
import qrcode
import io
import base64

router = APIRouter(prefix="/tracking", tags=["QR Takip"])


@router.post("/scan", response_model=QRScanResponse)
def scan_qr_code(
    scan_data: QRScanRequest,
    db: Session = Depends(get_db)
):
    """
    QR kod taramasını işle ve durum güncelle.
    Durum döngüsü: Hazırlandı → Yüklendi → Kuruldu → Toplandı
    """
    engine = StatusEngine(db)
    result = engine.process_qr_scan(
        qr_kodu=scan_data.qr_kodu,
        etkinlik_id=scan_data.etkinlik_id,
        personel_notu=scan_data.personel_notu
    )
    return result


@router.get("/event/{etkinlik_id}/status")
def get_event_status(
    etkinlik_id: int,
    db: Session = Depends(get_db)
):
    """Bir etkinliğin tüm ekipman durumlarını getir."""
    event = db.query(Event).filter(Event.id == etkinlik_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")

    engine = StatusEngine(db)
    progress = engine.get_event_progress(etkinlik_id)
    can_complete = engine.can_complete_event(etkinlik_id)

    items = db.query(ChecklistItem).filter(
        ChecklistItem.etkinlik_id == etkinlik_id
    ).all()

    item_details = []
    for item in items:
        inv = db.query(InventoryItem).filter(
            InventoryItem.id == item.envanter_id
        ).first()
        item_details.append({
            'id': item.id,
            'envanter_adi': inv.adi if inv else 'Bilinmiyor',
            'kategori': inv.kategori if inv else '',
            'qr_kodu': inv.qr_kodu if inv else '',
            'adet': item.adet,
            'durum': item.durum,
            'hazirlandi': item.hazirlandi_zamani,
            'yuklendi': item.yuklendi_zamani,
            'kuruldu': item.kuruldu_zamani,
            'toplandi': item.toplandi_zamani,
            'personel_notu': item.personel_notu
        })

    return {
        'etkinlik': {
            'id': event.id,
            'ad': event.etkinlik_adi,
            'tarih': event.tarih,
            'mekan': event.mekan,
            'durum': event.durum
        },
        'ilerleme': progress,
        'tamamlanabilir': can_complete,
        'ekipmanlar': item_details
    }


@router.post("/event/{etkinlik_id}/complete")
def complete_event(
    etkinlik_id: int,
    db: Session = Depends(get_db)
):
    """
    Etkinliği 'Tamamlandı' olarak işaretle.
    Tüm kalemler 'Toplandı' olmadan tamamlanamaz.
    """
    event = db.query(Event).filter(Event.id == etkinlik_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")

    engine = StatusEngine(db)
    check = engine.can_complete_event(etkinlik_id)

    if not check['tamamlanabilir']:
        raise HTTPException(
            status_code=400,
            detail=f"Etkinlik tamamlanamaz: {check['mesaj']}. Bekleyen: {check['bekleyen']}"
        )

    event.durum = "Tamamlandı"
    db.commit()

    return {
        'basarili': True,
        'mesaj': f'🎉 {event.etkinlik_adi} başarıyla tamamlandı!',
        'etkinlik_id': etkinlik_id
    }


@router.get("/generate-qr/{qr_kodu}")
def generate_qr_image(qr_kodu: str):
    """QR kod için base64 PNG resmi üret."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_kodu)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return {
        'qr_kodu': qr_kodu,
        'image_base64': f'data:image/png;base64,{img_base64}'
    }


@router.post("/checklist/add")
def add_to_checklist(
    item: ChecklistItemCreate,
    db: Session = Depends(get_db)
):
    """Etkinlik çeki listesine ekipman ekle (stok kontrolü ile)."""
    event = db.query(Event).filter(Event.id == item.etkinlik_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")

    inventory = db.query(InventoryItem).filter(
        InventoryItem.id == item.envanter_id
    ).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Envanter kalemi bulunamadı")

    # Stok kontrolü
    manager = StockManager(db)
    availability = manager.check_availability(
        inventory_id=item.envanter_id,
        event_date=event.tarih,
        requested_qty=item.adet
    )

    if not availability['musait']:
        raise HTTPException(
            status_code=409,
            detail=f"Stok yetersiz: {availability['mesaj']}"
        )

    # Zaten eklenmiş mi kontrol et
    existing = db.query(ChecklistItem).filter(
        ChecklistItem.etkinlik_id == item.etkinlik_id,
        ChecklistItem.envanter_id == item.envanter_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Bu ekipman zaten çeki listesine eklenmiş"
        )

    from datetime import datetime
    db_item = ChecklistItem(
        etkinlik_id=item.etkinlik_id,
        envanter_id=item.envanter_id,
        adet=item.adet,
        durum="Hazırlandı",
        hazirlandi_zamani=datetime.utcnow()
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return {
        'mesaj': f'✅ {inventory.adi} çeki listesine eklendi',
        'item_id': db_item.id,
        'musait_kalan': availability['musait_adet'] - item.adet
    }


@router.delete("/checklist/{item_id}")
def remove_from_checklist(item_id: int, db: Session = Depends(get_db)):
    """Çeki listesinden ekipman kaldır."""
    item = db.query(ChecklistItem).filter(ChecklistItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Çeki listesi kalemi bulunamadı")

    db.delete(item)
    db.commit()
    return {'mesaj': 'Kalem çeki listesinden kaldırıldı'}
