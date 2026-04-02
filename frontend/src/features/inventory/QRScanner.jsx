import React, { useEffect, useState } from 'react';
import { Html5QrcodeScanner } from 'html5-qrcode';
import api from '../../api/axios';
import { QrCode, CheckCircle2, AlertCircle } from 'lucide-react';
import StatusBadge from '../../components/StatusBadge';

const QRScanner = () => {
  const [scanResult, setScanResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  // Default to active event id (Mock) - in real life, select from active events
  const [activeEventId, setActiveEventId] = useState(1); 

  useEffect(() => {
    const scanner = new Html5QrcodeScanner(
      "reader",
      { fps: 10, qrbox: { width: 250, height: 250 } },
      /* verbose= */ false
    );

    scanner.render(onScanSuccess, onScanFailure);

    return () => {
      scanner.clear().catch(error => console.error("Failed to clear scanner", error));
    };
  }, [activeEventId]);

  const onScanSuccess = async (decodedText) => {
    try {
      setLoading(true);
      setError(null);
      // Backend call to process scan
      const response = await api.post('/tracking/scan', {
        qr_kodu: decodedText,
        etkinlik_id: activeEventId
      });
      
      setScanResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Karekod okunamadı veya sunucu hatası!");
    } finally {
      setLoading(false);
    }
  };

  const onScanFailure = (error) => {
    // Ignore routine failures
  };

  return (
    <div className="max-w-md mx-auto">
      <div className="bg-primary-DEFAULT text-white p-6 rounded-t-xl text-center">
        <QrCode className="w-12 h-12 mx-auto mb-3 text-accent-DEFAULT" />
        <h2 className="text-xl font-bold">Ekipman Tarayıcı</h2>
        <p className="text-sm text-gray-300 mt-1">
          Durumu güncellemek için QR kodu kameraya gösterin.
        </p>
      </div>

      <div className="bg-white p-6 rounded-b-xl shadow-md border border-gray-100">
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Aktif Etkinlik</label>
          <select 
            className="input-field" 
            value={activeEventId} 
            onChange={(e) => setActiveEventId(Number(e.target.value))}
          >
            <option value={1}>Yılmaz & Demir Düğünü</option>
            <option value={2}>Arslan & Kaya Nişanı</option>
            <option value={3}>TechCorp Kurumsal Gala</option>
          </select>
        </div>

        {/* Scanner Mount Point */}
        <div id="reader" className="w-full overflow-hidden rounded-lg outline-none max-w-sm mx-auto"></div>
        
        {loading && (
          <div className="mt-6 text-center text-primary-DEFAULT font-medium animate-pulse">
            İşleniyor...
          </div>
        )}

        {/* Results Info */}
        {scanResult && !loading && (
          <div className={`mt-6 p-4 rounded-xl border ${scanResult.basarili ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
            <div className="flex items-start gap-3">
              {scanResult.basarili ? (
                <CheckCircle2 className="w-6 h-6 text-green-600 shrink-0 mt-0.5" />
              ) : (
                <AlertCircle className="w-6 h-6 text-red-600 shrink-0 mt-0.5" />
              )}
              <div>
                <h4 className={`font-semibold ${scanResult.basarili ? 'text-green-800' : 'text-red-800'}`}>
                  {scanResult.envanter_adi || "İşlem Başarısız"}
                </h4>
                <p className={`text-sm mt-1 ${scanResult.basarili ? 'text-green-700' : 'text-red-700'}`}>
                  {scanResult.mesaj}
                </p>
                {scanResult.basarili && scanResult.onceki_durum !== scanResult.yeni_durum && (
                  <div className="flex items-center gap-2 mt-3 text-sm">
                    <StatusBadge status={scanResult.onceki_durum} />
                    <span className="text-gray-400">➔</span>
                    <StatusBadge status={scanResult.yeni_durum} />
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {error && !loading && (
          <div className="mt-6 p-4 rounded-xl bg-red-50 border border-red-200 flex items-start gap-3">
             <AlertCircle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
             <p className="text-sm text-red-700">{error}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default QRScanner;
