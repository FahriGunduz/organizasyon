"""
EOS - Planning API
Etkinlik planlama, müşteri ve envanter yönetim endpoint'leri.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app.models.event import Event
from app.models.customer import Customer
from app.models.inventory import InventoryItem
from app.models.checklist import ChecklistItem
from app.schemas.event import EventCreate, EventUpdate, EventResponse, EventDetailResponse
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from app.services.stock_manager import StockManager

router = APIRouter(prefix="/planning", tags=["Planlama"])


# ===== CUSTOMERS =====

@router.get("/customers", response_model=List[CustomerResponse])
def get_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Tüm müşterileri listele."""
    return db.query(Customer).offset(skip).limit(limit).all()


@router.post("/customers", response_model=CustomerResponse, status_code=201)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """Yeni müşteri ekle."""
    if customer.tc_no:
        existing = db.query(Customer).filter(Customer.tc_no == customer.tc_no).first()
        if existing:
            raise HTTPException(status_code=409, detail="Bu TC No zaten kayıtlı")

    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Müşteri detayını getir."""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    return customer


@router.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db)
):
    """Müşteri bilgilerini güncelle."""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")

    update_data = customer_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer


# ===== EVENTS =====

@router.get("/events", response_model=List[EventDetailResponse])
def get_events(
    durum: Optional[str] = None,
    firma: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Etkinlikleri listele (filtre ile)."""
    query = db.query(Event)

    if durum:
        query = query.filter(Event.durum == durum)
    if firma:
        query = query.filter(Event.sorumlu_firma == firma)

    events = query.order_by(Event.tarih.desc()).all()

    result = []
    for event in events:
        customer = db.query(Customer).filter(Customer.id == event.musteri_id).first()
        checklist_items = db.query(ChecklistItem).filter(
            ChecklistItem.etkinlik_id == event.id
        ).all()

        total = len(checklist_items)
        completed = sum(1 for i in checklist_items if i.durum == "Toplandı")

        result.append(EventDetailResponse(
            id=event.id,
            etkinlik_adi=event.etkinlik_adi,
            musteri_id=event.musteri_id,
            tarih=event.tarih,
            mekan=event.mekan,
            mekan_giris_saati=event.mekan_giris_saati,
            mekan_cikis_saati=event.mekan_cikis_saati,
            etkinlik_turu=event.etkinlik_turu,
            durum=event.durum,
            sorumlu_firma=event.sorumlu_firma,
            ekip_sayisi=event.ekip_sayisi,
            misafir_sayisi=event.misafir_sayisi,
            notlar=event.notlar,
            created_at=event.created_at,
            updated_at=event.updated_at,
            musteri_adi=f"{customer.ad} {customer.soyad}" if customer else None,
            toplam_ekipman=total,
            tamamlanan_ekipman=completed,
            ilerleme_yuzdesi=round((completed / total * 100) if total > 0 else 0, 1)
        ))

    return result


@router.post("/events", response_model=EventResponse, status_code=201)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """Yeni etkinlik oluştur."""
    customer = db.query(Customer).filter(Customer.id == event.musteri_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")

    db_event = Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/events/{event_id}")
def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    """Etkinlik detayını getir (müşteri, çeki listesi, finans dahil)."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")

    customer = db.query(Customer).filter(Customer.id == event.musteri_id).first()
    checklist_items = db.query(ChecklistItem).filter(
        ChecklistItem.etkinlik_id == event_id
    ).all()

    items_detail = []
    for item in checklist_items:
        inv = db.query(InventoryItem).filter(InventoryItem.id == item.envanter_id).first()
        items_detail.append({
            'id': item.id,
            'envanter': {
                'id': inv.id if inv else None,
                'adi': inv.adi if inv else 'Bilinmiyor',
                'kategori': inv.kategori if inv else '',
                'qr_kodu': inv.qr_kodu if inv else '',
                'firma': inv.firma if inv else ''
            },
            'adet': item.adet,
            'durum': item.durum,
            'personel_notu': item.personel_notu
        })

    return {
        'etkinlik': {
            'id': event.id,
            'etkinlik_adi': event.etkinlik_adi,
            'tarih': event.tarih,
            'mekan': event.mekan,
            'mekan_giris_saati': event.mekan_giris_saati,
            'mekan_cikis_saati': event.mekan_cikis_saati,
            'etkinlik_turu': event.etkinlik_turu,
            'durum': event.durum,
            'sorumlu_firma': event.sorumlu_firma,
            'ekip_sayisi': event.ekip_sayisi,
            'misafir_sayisi': event.misafir_sayisi,
            'notlar': event.notlar
        },
        'musteri': {
            'id': customer.id,
            'ad': f"{customer.ad} {customer.soyad}",
            'telefon': customer.telefon,
            'email': customer.email
        } if customer else None,
        'checklist': items_detail
    }


@router.put("/events/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: Session = Depends(get_db)
):
    """Etkinlik bilgilerini güncelle."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")

    update_data = event_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)

    db.commit()
    db.refresh(event)
    return event


# ===== INVENTORY =====

@router.get("/inventory", response_model=List[InventoryResponse])
def get_inventory(
    firma: Optional[str] = None,
    kategori: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Envanter listesini getir."""
    query = db.query(InventoryItem).filter(InventoryItem.aktif == 1)

    if firma:
        query = query.filter(InventoryItem.firma == firma)
    if kategori:
        query = query.filter(InventoryItem.kategori == kategori)

    return query.all()


@router.get("/inventory/availability/{tarih}")
def get_inventory_availability(tarih: str, db: Session = Depends(get_db)):
    """Belirli bir tarih için tüm envanterin uygunluk durumunu getir."""
    manager = StockManager(db)
    return manager.get_inventory_summary_for_date(tarih)


@router.post("/inventory", response_model=InventoryResponse, status_code=201)
def create_inventory(item: InventoryCreate, db: Session = Depends(get_db)):
    """Yeni envanter kalemi ekle."""
    existing = db.query(InventoryItem).filter(
        InventoryItem.qr_kodu == item.qr_kodu
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Bu QR kod zaten kullanımda")

    db_item = InventoryItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/inventory/{item_id}", response_model=InventoryResponse)
def update_inventory(
    item_id: int,
    item_update: InventoryUpdate,
    db: Session = Depends(get_db)
):
    """Envanter kalemi güncelle."""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Envanter kalemi bulunamadı")

    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.get("/inventory/{item_id}/check")
def check_inventory_availability(
    item_id: int,
    tarih: str = Query(..., description="YYYY-MM-DD format"),
    adet: int = Query(1, description="İstenen miktar"),
    db: Session = Depends(get_db)
):
    """Belirli bir tarih için envanter uygunluğunu kontrol et."""
    manager = StockManager(db)
    return manager.check_availability(item_id, tarih, adet)
