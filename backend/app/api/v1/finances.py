"""
EOS - Finance API
Sözleşme ve ödeme takip endpoint'leri.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models.finance import Finance
from app.models.event import Event
from app.schemas.finance import FinanceCreate, FinanceUpdate, FinanceResponse

router = APIRouter(prefix="/finances", tags=["Finans"])


@router.get("/", response_model=List[FinanceResponse])
def get_finances(db: Session = Depends(get_db)):
    """Tüm finans kayıtlarını listele."""
    finances = db.query(Finance).all()
    result = []
    for f in finances:
        event = db.query(Event).filter(Event.id == f.etkinlik_id).first()
        data = FinanceResponse(
            id=f.id,
            etkinlik_id=f.etkinlik_id,
            toplam_tutar=f.toplam_tutar,
            kapora=f.kapora,
            kalan_odeme=f.kalan_odeme,
            odeme_tarihi=f.odeme_tarihi,
            sozlesme_tarihi=f.sozlesme_tarihi,
            durum=f.durum,
            odeme_yontemi=f.odeme_yontemi,
            fatura_no=f.fatura_no,
            notlar=f.notlar,
            created_at=f.created_at,
            updated_at=f.updated_at,
            etkinlik_adi=event.etkinlik_adi if event else None
        )
        result.append(data)
    return result


@router.post("/", response_model=FinanceResponse, status_code=201)
def create_finance(finance: FinanceCreate, db: Session = Depends(get_db)):
    """Etkinlik için finans/sözleşme kaydı oluştur."""
    event = db.query(Event).filter(Event.id == finance.etkinlik_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")

    # Kalan ödemeyi otomatik hesapla
    data = finance.model_dump()
    if data.get('kalan_odeme') is None:
        data['kalan_odeme'] = data['toplam_tutar'] - (data.get('kapora') or 0)

    db_finance = Finance(**data)
    db.add(db_finance)
    db.commit()
    db.refresh(db_finance)

    return FinanceResponse(
        **{c.name: getattr(db_finance, c.name) for c in Finance.__table__.columns},
        etkinlik_adi=event.etkinlik_adi
    )


@router.get("/{finance_id}", response_model=FinanceResponse)
def get_finance(finance_id: int, db: Session = Depends(get_db)):
    """Finans kaydı detayını getir."""
    finance = db.query(Finance).filter(Finance.id == finance_id).first()
    if not finance:
        raise HTTPException(status_code=404, detail="Finans kaydı bulunamadı")

    event = db.query(Event).filter(Event.id == finance.etkinlik_id).first()
    return FinanceResponse(
        **{c.name: getattr(finance, c.name) for c in Finance.__table__.columns},
        etkinlik_adi=event.etkinlik_adi if event else None
    )


@router.put("/{finance_id}", response_model=FinanceResponse)
def update_finance(
    finance_id: int,
    finance_update: FinanceUpdate,
    db: Session = Depends(get_db)
):
    """Ödeme durumunu güncelle."""
    finance = db.query(Finance).filter(Finance.id == finance_id).first()
    if not finance:
        raise HTTPException(status_code=404, detail="Finans kaydı bulunamadı")

    update_data = finance_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(finance, field, value)

    # Kalan ödemeyi güncelle
    if 'kapora' in update_data or 'toplam_tutar' in update_data:
        finance.kalan_odeme = finance.toplam_tutar - (finance.kapora or 0)

    db.commit()
    db.refresh(finance)

    event = db.query(Event).filter(Event.id == finance.etkinlik_id).first()
    return FinanceResponse(
        **{c.name: getattr(finance, c.name) for c in Finance.__table__.columns},
        etkinlik_adi=event.etkinlik_adi if event else None
    )


@router.get("/summary/overview")
def get_finance_summary(db: Session = Depends(get_db)):
    """Finansal genel bakış istatistiklerini döndür."""
    finances = db.query(Finance).all()

    total_revenue = sum(f.toplam_tutar for f in finances)
    total_collected = sum(f.kapora or 0 for f in finances)
    total_pending = sum(f.kalan_odeme or 0 for f in finances)

    by_status = {}
    for f in finances:
        by_status[f.durum] = by_status.get(f.durum, 0) + 1

    return {
        'toplam_gelir': total_revenue,
        'tahsil_edilen': total_collected,
        'bekleyen_tahsilat': total_pending,
        'durum_dagilimi': by_status,
        'sozlesme_sayisi': len(finances)
    }
