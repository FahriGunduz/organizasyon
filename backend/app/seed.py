"""
EOS - Demo Seed Data
La Vita Bella Event İzmir ve Umut Aybar Organizasyon firmaları için
hazır demo verileri oluşturur.
"""

from datetime import datetime
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.models.inventory import InventoryItem
from app.models.event import Event
from app.models.checklist import ChecklistItem
from app.models.finance import Finance


def seed_database(db: Session):
    """Eğer veritabanı boşsa demo verilerini yükle."""

    # Zaten veri varsa seed etme
    if db.query(Customer).count() > 0:
        print("✅ Demo verileri zaten mevcut, seed atlanıyor.")
        return

    print("🌱 Demo verileri yükleniyor...")

    # ===== MÜŞTERİLER =====
    customers = [
        Customer(
            tc_no="12345678901",
            ad="Ayşe Gül",
            soyad="Yılmaz",
            telefon="0532 111 2233",
            email="aysegul@email.com",
            adres="Alsancak Mah. Kıbrıs Şehitleri Cad. No:45 Konak/İzmir",
            firma_turu="Bireysel",
            notlar="Gelin - Yılmaz & Demir Düğünü"
        ),
        Customer(
            tc_no="98765432109",
            ad="Mert",
            soyad="Arslan",
            telefon="0533 444 5566",
            email="mert.arslan@email.com",
            adres="Bornova Mah. Atatürk Cad. No:12 Bornova/İzmir",
            firma_turu="Bireysel",
            notlar="Damat - Arslan & Kaya Nişanı"
        ),
        Customer(
            tc_no=None,
            ad="Teknoloji A.Ş.",
            soyad="",
            telefon="0232 333 4455",
            email="etkinlik@techcorp.com.tr",
            adres="Atatürk Organize Sanayi Böl. İzmir",
            firma_turu="Kurumsal",
            firma_adi="TechCorp Teknoloji A.Ş.",
            notlar="Kurumsal yıllık gala organizasyonu"
        ),
        Customer(
            tc_no="55544433322",
            ad="Fatma",
            soyad="Demir",
            telefon="0535 777 8899",
            email="fatma.demir@gmail.com",
            adres="Karşıyaka Mah. Birinci Sok. No:8 Karşıyaka/İzmir",
            firma_turu="Bireysel",
            notlar="Gelin - Yılmaz & Demir Düğünü (Damat tarafı müşteri)"
        ),
    ]

    for c in customers:
        db.add(c)
    db.flush()

    # ===== ENVANTER (12 kalem) =====
    inventory_items = [
        # La Vita Bella Envanteri
        InventoryItem(
            adi="Kristal Şamdan (Uzun Boy)",
            kategori="Dekorasyon",
            toplam_adet=20,
            firma="La Vita Bella",
            qr_kodu="LVB-SHM-001",
            aciklama="60cm yükseklik, kristal şamdan - masa merkezi dekorasyonu",
            birim_fiyat=150.0
        ),
        InventoryItem(
            adi="Tül Perde Takımı (Beyaz)",
            kategori="Tekstil",
            toplam_adet=15,
            firma="La Vita Bella",
            qr_kodu="LVB-TUL-002",
            aciklama="Gelin yolu ve sahne perdesi için 5m x 3m beyaz tül",
            birim_fiyat=200.0
        ),
        InventoryItem(
            adi="Gelin Yolu Halısı (Beyaz)",
            kategori="Tekstil",
            toplam_adet=8,
            firma="La Vita Bella",
            qr_kodu="LVB-HLI-003",
            aciklama="10m uzunluk, 1.5m genişlik, roll halı",
            birim_fiyat=300.0
        ),
        InventoryItem(
            adi="Nişan/Söz Tepsisi Seti",
            kategori="Dekorasyon",
            toplam_adet=10,
            firma="La Vita Bella",
            qr_kodu="LVB-TEP-004",
            aciklama="6 parçalı gümüş kaplama nişan tepsisi seti",
            birim_fiyat=500.0
        ),
        InventoryItem(
            adi="Fotoğraf Köşesi Çerçeve Seti",
            kategori="Dekorasyon",
            toplam_adet=4,
            firma="La Vita Bella",
            qr_kodu="LVB-FOT-005",
            aciklama="Ahşap büyük çerçeve, balon garland, çiçek standı",
            birim_fiyat=800.0
        ),
        # Umut Aybar Envanteri
        InventoryItem(
            adi="Chiavari Sandalye (Beyaz/Altın)",
            kategori="Mobilya",
            toplam_adet=200,
            firma="Umut Aybar",
            qr_kodu="UA-SND-001",
            aciklama="Lüks düğün sandalyesi, metaller altın kaplamalı",
            birim_fiyat=25.0
        ),
        InventoryItem(
            adi="Profesyonel Ses Sistemi Seti",
            kategori="Teknik/Ses",
            toplam_adet=3,
            firma="Umut Aybar",
            qr_kodu="UA-SES-002",
            aciklama="2x Subwoofer + 4x Column hoparlör, mikser, mikrofon seti",
            birim_fiyat=5000.0
        ),
        InventoryItem(
            adi="LED Aydınlatma Armatürü (Moving Head)",
            kategori="Aydınlatma",
            toplam_adet=12,
            firma="Umut Aybar",
            qr_kodu="UA-AYD-003",
            aciklama="Hareketli kafa LED ışık sistemi, DMX kontrollu",
            birim_fiyat=1200.0
        ),
        # Ortak Envanter
        InventoryItem(
            adi="LED Işık Zinciri (10m)",
            kategori="Aydınlatma",
            toplam_adet=50,
            firma="Ortak",
            qr_kodu="ORK-LED-001",
            aciklama="Warm white LED peri ışığı, 10 metre",
            birim_fiyat=80.0
        ),
        InventoryItem(
            adi="Masa Örtüsü (Krem/Saten)",
            kategori="Tekstil",
            toplam_adet=100,
            firma="Ortak",
            qr_kodu="ORK-ORT-002",
            aciklama="180cm yuvarlak masa için krem saten örtü",
            birim_fiyat=50.0
        ),
        InventoryItem(
            adi="Balon Standı ve Garland Seti",
            kategori="Dekorasyon",
            toplam_adet=30,
            firma="Ortak",
            qr_kodu="ORK-BAL-003",
            aciklama="Krom balon standı + 100 adet balon kiti",
            birim_fiyat=120.0
        ),
        InventoryItem(
            adi="Çiçek Standı (Metal, Altın Kaplama)",
            kategori="Dekorasyon",
            toplam_adet=25,
            firma="Ortak",
            qr_kodu="ORK-CIC-004",
            aciklama="1.2m yükseklik altın kaplama metal çiçek standı",
            birim_fiyat=180.0
        ),
    ]

    for item in inventory_items:
        db.add(item)
    db.flush()

    # ===== ETKİNLİKLER (3 aktif etkinlik) =====
    events = [
        Event(
            etkinlik_adi="Yılmaz & Demir Düğünü",
            musteri_id=customers[0].id,
            tarih="2026-04-15",
            mekan="Kordon Palace Hotel - Büyük Salon",
            mekan_giris_saati="08:00",
            mekan_cikis_saati="02:00",
            etkinlik_turu="Düğün",
            durum="Aktif",
            sorumlu_firma="La Vita Bella",
            ekip_sayisi=8,
            misafir_sayisi=250,
            notlar="Gelin rengi: Krem & Altın. Özel gelin yolu istiyor. Tüm LED ışıklar warm white."
        ),
        Event(
            etkinlik_adi="Arslan & Kaya Nişanı",
            musteri_id=customers[1].id,
            tarih="2026-04-20",
            mekan="Çeşme Altın Yunus Kır Bahçesi",
            mekan_giris_saati="14:00",
            mekan_cikis_saati="23:00",
            etkinlik_turu="Nişan",
            durum="Planlandı",
            sorumlu_firma="Umut Aybar",
            ekip_sayisi=5,
            misafir_sayisi=80,
            notlar="Açık hava nişan. Rüzgara karşı dayanıklı dekorasyon tercih edilmeli."
        ),
        Event(
            etkinlik_adi="TechCorp Kurumsal Gala 2026",
            musteri_id=customers[2].id,
            tarih="2026-04-25",
            mekan="İzmir Fuar Alanı - Kongre Merkezi",
            mekan_giris_saati="10:00",
            mekan_cikis_saati="00:00",
            etkinlik_turu="Kurumsal",
            durum="Planlandı",
            sorumlu_firma="Ortak",
            ekip_sayisi=12,
            misafir_sayisi=450,
            notlar="Her iki firma ortak operasyon. Kurumsal renk: Lacivert & Gümüş."
        ),
    ]

    for event in events:
        db.add(event)
    db.flush()

    # ===== ÇEKİ LİSTESİ KALEMLERİ =====
    checklist_items = [
        # Etkinlik 1: Yılmaz & Demir Düğünü
        ChecklistItem(
            etkinlik_id=events[0].id,
            envanter_id=inventory_items[0].id,  # Kristal Şamdan
            adet=15,
            durum="Kuruldu",
            hazirlandi_zamani=datetime(2026, 4, 15, 6, 0),
            yuklendi_zamani=datetime(2026, 4, 15, 7, 30),
            kuruldu_zamani=datetime(2026, 4, 15, 9, 15),
        ),
        ChecklistItem(
            etkinlik_id=events[0].id,
            envanter_id=inventory_items[1].id,  # Tül Perde
            adet=6,
            durum="Kuruldu",
            hazirlandi_zamani=datetime(2026, 4, 15, 6, 0),
            yuklendi_zamani=datetime(2026, 4, 15, 7, 30),
            kuruldu_zamani=datetime(2026, 4, 15, 9, 45),
        ),
        ChecklistItem(
            etkinlik_id=events[0].id,
            envanter_id=inventory_items[2].id,  # Gelin Yolu
            adet=2,
            durum="Yüklendi",
            hazirlandi_zamani=datetime(2026, 4, 15, 6, 30),
            yuklendi_zamani=datetime(2026, 4, 15, 7, 30),
        ),
        ChecklistItem(
            etkinlik_id=events[0].id,
            envanter_id=inventory_items[8].id,  # LED Zincir
            adet=20,
            durum="Kuruldu",
            hazirlandi_zamani=datetime(2026, 4, 15, 6, 0),
            yuklendi_zamani=datetime(2026, 4, 15, 7, 30),
            kuruldu_zamani=datetime(2026, 4, 15, 9, 0),
        ),
        ChecklistItem(
            etkinlik_id=events[0].id,
            envanter_id=inventory_items[9].id,  # Masa Örtüsü
            adet=30,
            durum="Yüklendi",
            hazirlandi_zamani=datetime(2026, 4, 15, 6, 0),
            yuklendi_zamani=datetime(2026, 4, 15, 7, 30),
        ),
        # Etkinlik 2: Arslan & Kaya Nişanı
        ChecklistItem(
            etkinlik_id=events[1].id,
            envanter_id=inventory_items[3].id,  # Nişan Tepsisi
            adet=3,
            durum="Hazırlandı",
            hazirlandi_zamani=datetime(2026, 4, 20, 12, 0),
        ),
        ChecklistItem(
            etkinlik_id=events[1].id,
            envanter_id=inventory_items[10].id,  # Balon Standı
            adet=8,
            durum="Hazırlandı",
            hazirlandi_zamani=datetime(2026, 4, 20, 12, 0),
        ),
        ChecklistItem(
            etkinlik_id=events[1].id,
            envanter_id=inventory_items[11].id,  # Çiçek Standı
            adet=10,
            durum="Hazırlandı",
            hazirlandi_zamani=datetime(2026, 4, 20, 12, 0),
        ),
        # Etkinlik 3: TechCorp Gala
        ChecklistItem(
            etkinlik_id=events[2].id,
            envanter_id=inventory_items[5].id,  # Sandalye
            adet=150,
            durum="Hazırlandı",
        ),
        ChecklistItem(
            etkinlik_id=events[2].id,
            envanter_id=inventory_items[6].id,  # Ses Sistemi
            adet=2,
            durum="Hazırlandı",
        ),
        ChecklistItem(
            etkinlik_id=events[2].id,
            envanter_id=inventory_items[7].id,  # Moving Head LED
            adet=8,
            durum="Hazırlandı",
        ),
        ChecklistItem(
            etkinlik_id=events[2].id,
            envanter_id=inventory_items[8].id,  # LED Zincir
            adet=15,
            durum="Hazırlandı",
        ),
        ChecklistItem(
            etkinlik_id=events[2].id,
            envanter_id=inventory_items[9].id,  # Masa Örtüsü
            adet=50,
            durum="Hazırlandı",
        ),
    ]

    for cl_item in checklist_items:
        db.add(cl_item)
    db.flush()

    # ===== FİNANS KAYITLARI =====
    finances = [
        Finance(
            etkinlik_id=events[0].id,
            toplam_tutar=45000.0,
            kapora=15000.0,
            kalan_odeme=30000.0,
            odeme_tarihi="2026-04-15",
            sozlesme_tarihi="2026-03-01",
            durum="Kısmi Ödeme",
            odeme_yontemi="Havale",
            fatura_no="LVB-2026-001",
            notlar="Kapora 15.000 TL tahsil edildi. Kalan etkinlik günü ödenecek."
        ),
        Finance(
            etkinlik_id=events[1].id,
            toplam_tutar=18000.0,
            kapora=5000.0,
            kalan_odeme=13000.0,
            odeme_tarihi="2026-04-20",
            sozlesme_tarihi="2026-03-15",
            durum="Kısmi Ödeme",
            odeme_yontemi="Nakit",
            fatura_no="UA-2026-008",
            notlar="5.000 TL kapora alındı."
        ),
        Finance(
            etkinlik_id=events[2].id,
            toplam_tutar=85000.0,
            kapora=25000.0,
            kalan_odeme=60000.0,
            odeme_tarihi="2026-04-25",
            sozlesme_tarihi="2026-03-20",
            durum="Kısmi Ödeme",
            odeme_yontemi="Havale",
            fatura_no="ORK-2026-002",
            notlar="Kurumsal fatura düzenlenecek. KDV dahil fiyat."
        ),
    ]

    for fin in finances:
        db.add(fin)

    db.commit()
    print("✅ Demo verileri başarıyla yüklendi!")
    print(f"   👥 {len(customers)} müşteri")
    print(f"   📦 {len(inventory_items)} envanter kalemi")
    print(f"   🎪 {len(events)} aktif etkinlik")
    print(f"   📋 {len(checklist_items)} çeki listesi kalemi")
    print(f"   💰 {len(finances)} finans kaydı")
