"""
EOS - Entegre Organizasyon Yönetim Sistemi
Ana FastAPI Uygulaması

La Vita Bella Event İzmir & Umut Aybar Organizasyon
Operasyonel hata oranını %0'a indiren QR tabanlı yönetim sistemi.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, SessionLocal
from app.models import customer, inventory, event, checklist, finance
from app.api.v1 import tracking, planning, finances
from app.seed import seed_database

# Tabloları oluştur
customer.Base.metadata.create_all(bind=engine)
inventory.Base.metadata.create_all(bind=engine)
event.Base.metadata.create_all(bind=engine)
checklist.Base.metadata.create_all(bind=engine)
finance.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EOS - Entegre Organizasyon Yönetim Sistemi",
    description="""
    ## La Vita Bella Event İzmir & Umut Aybar Organizasyon

    Kağıt listelerden kaynaklanan operasyonel hataları **%0'a indiren** 
    QR kod tabanlı entegre yönetim sistemi.

    ### Özellikler:
    - 📦 **Akıllı Rezervasyon**: Stok çakışma kontrolü
    - 📱 **QR Durum Döngüsü**: Hazırlandı → Yüklendi → Kuruldu → Toplandı
    - 🔒 **Saha Onayı**: Tüm ekipmanlar toplanmadan etkinlik tamamlanamaz
    - 💰 **Finans Takibi**: Sözleşme ve ödeme yönetimi
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS - Frontend erişimi için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Router'ları kaydet
app.include_router(tracking.router, prefix="/api/v1")
app.include_router(planning.router, prefix="/api/v1")
app.include_router(finances.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Uygulama başlangıcında demo verilerini yükle."""
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


@app.get("/", tags=["Root"])
def root():
    """EOS API Health Check."""
    return {
        "sistem": "EOS - Entegre Organizasyon Yönetim Sistemi",
        "versiyon": "1.0.0",
        "durum": "🟢 Aktif",
        "firmalar": ["La Vita Bella Event İzmir", "Umut Aybar Organizasyon"],
        "docs": "/docs"
    }


@app.get("/api/v1/dashboard/stats", tags=["Dashboard"])
def get_dashboard_stats(db=None):
    """Genel istatistikler."""
    from app.database import get_db
    from app.models.event import Event as EventModel
    from app.models.customer import Customer as CustomerModel
    from app.models.inventory import InventoryItem as InventoryModel
    from app.models.checklist import ChecklistItem as ChecklistModel
    from app.models.finance import Finance as FinanceModel
    from sqlalchemy.orm import Session
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        total_events = db.query(EventModel).count()
        active_events = db.query(EventModel).filter(EventModel.durum == "Aktif").count()
        planned_events = db.query(EventModel).filter(EventModel.durum == "Planlandı").count()
        total_customers = db.query(CustomerModel).count()
        total_inventory = db.query(InventoryModel).count()

        finances = db.query(FinanceModel).all()
        total_revenue = sum(f.toplam_tutar for f in finances)
        collected = sum(f.kapora or 0 for f in finances)

        checklist_items = db.query(ChecklistModel).all()
        total_items = len(checklist_items)
        completed_items = sum(1 for i in checklist_items if i.durum == "Toplandı")

        return {
            "etkinlikler": {
                "toplam": total_events,
                "aktif": active_events,
                "planlandı": planned_events,
            },
            "musteriler": total_customers,
            "envanter": total_inventory,
            "finans": {
                "toplam_gelir": total_revenue,
                "tahsil_edilen": collected,
                "bekleyen": total_revenue - collected
            },
            "operasyon": {
                "toplam_ekipman": total_items,
                "tamamlanan": completed_items,
                "ilerleme": round((completed_items / total_items * 100) if total_items > 0 else 0, 1)
            }
        }
    finally:
        db.close()
