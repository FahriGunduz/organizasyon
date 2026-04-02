import React, { useState, useEffect } from 'react';
import api from '../../api/axios';
import { Wallet, Plus, Save, FileText, CheckCircle } from 'lucide-react';
import StatusBadge from '../../components/StatusBadge';

const Finance = () => {
  const [finances, setFinances] = useState([]);
  const [events, setEvents] = useState([]);
  const [financeForm, setFinanceForm] = useState({ etkinlik_id: '', toplam_tutar: '', kapora: '', odeme_yontemi: 'Havale', notlar: '' });
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [finRes, evtRes] = await Promise.all([
        api.get('/finances/'),
        api.get('/planning/events')
      ]);
      setFinances(finRes.data);
      setEvents(evtRes.data);
      if (evtRes.data.length > 0) {
        setFinanceForm(prev => ({ ...prev, etkinlik_id: evtRes.data[0].id }));
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleFinanceSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/finances/', {
        ...financeForm,
        etkinlik_id: Number(financeForm.etkinlik_id),
        toplam_tutar: Number(financeForm.toplam_tutar),
        kapora: Number(financeForm.kapora),
        sozlesme_tarihi: new Date().toISOString().split('T')[0]
      });
      alert('Sözleşme ve Finans Kaydı oluşturuldu!');
      fetchData();
      setIsAdding(false);
      setFinanceForm({ ...financeForm, toplam_tutar: '', kapora: '', notlar: '' });
    } catch (err) {
      alert('Hata: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-primary-DEFAULT flex items-center gap-2">
          <Wallet className="w-6 h-6"/> Finans ve Sözleşmeler
        </h1>
        <button 
          onClick={() => setIsAdding(!isAdding)}
          className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors flex items-center gap-2 ${isAdding ? 'bg-gray-200 text-gray-700' : 'bg-primary-DEFAULT text-white'}`}>
          {isAdding ? "İptal" : <><Plus className="w-4 h-4" /> Yeni Ödeme Planı</>}
        </button>
      </div>

      {isAdding ? (
        <div className="card p-6 max-w-2xl mx-auto border-t-4 border-t-accent-DEFAULT">
          <h2 className="text-lg font-semibold mb-4 border-b pb-2 flex items-center gap-2"><FileText className="w-5 h-5"/> Sözleşme Oluştur</h2>
          <form onSubmit={handleFinanceSubmit} className="space-y-4">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Hangi Etkinlik? <span className="text-red-500">*</span></label>
              <select required className="input-field" value={financeForm.etkinlik_id} onChange={e => setFinanceForm({...financeForm, etkinlik_id: e.target.value})}>
                <option value="" disabled>Etkinlik Seçin</option>
                {events.map(ev => <option key={ev.id} value={ev.id}>{ev.etkinlik_adi} - {ev.tarih}</option>)}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-600 mb-1">Toplam Anlaşılan Tutar (₺) <span className="text-red-500">*</span></label>
                <input required className="input-field" type="number" min="0" value={financeForm.toplam_tutar} onChange={e => setFinanceForm({...financeForm, toplam_tutar: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Alınan Kapora (₺) <span className="text-red-500">*</span></label>
                <input required className="input-field" type="number" min="0" value={financeForm.kapora} onChange={e => setFinanceForm({...financeForm, kapora: e.target.value})} />
              </div>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Ödeme Yöntemi</label>
              <select className="input-field" value={financeForm.odeme_yontemi} onChange={e => setFinanceForm({...financeForm, odeme_yontemi: e.target.value})}>
                <option value="Havale">Havale / EFT</option>
                <option value="Nakit">Elden Nakit</option>
                <option value="Kredi Kartı">Kredi Kartı</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Sözleşme Notları</label>
              <textarea placeholder="Fatura kesilecek mi? İade koşulları vb." className="input-field min-h-[80px]" value={financeForm.notlar} onChange={e => setFinanceForm({...financeForm, notlar: e.target.value})}></textarea>
            </div>
            <button type="submit" className="btn-accent w-full mt-4 flex items-center justify-center gap-2"><Save className="w-4 h-4"/> Kaydet</button>
          </form>
        </div>
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="py-3 px-4 font-semibold text-gray-600 text-sm">Etkinlik</th>
                <th className="py-3 px-4 font-semibold text-gray-600 text-sm">Toplam (₺)</th>
                <th className="py-3 px-4 font-semibold text-gray-600 text-sm">Kapora (₺)</th>
                <th className="py-3 px-4 font-semibold text-gray-600 text-sm">Kalan (₺)</th>
                <th className="py-3 px-4 font-semibold text-gray-600 text-sm">Durum</th>
                <th className="py-3 px-4 font-semibold text-gray-600 text-sm">Notlar</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {finances.map((fin) => (
                <tr key={fin.id} className="hover:bg-gray-50 transition-colors">
                  <td className="py-3 px-4">
                    <div className="font-medium text-gray-900">{fin.etkinlik_adi}</div>
                    <div className="text-xs text-gray-500">Söz: {fin.sozlesme_tarihi}</div>
                  </td>
                  <td className="py-3 px-4 font-medium text-gray-900">₺{fin.toplam_tutar?.toLocaleString()}</td>
                  <td className="py-3 px-4 text-green-600 font-medium">+₺{fin.kapora?.toLocaleString()}</td>
                  <td className="py-3 px-4 text-red-600 font-medium">-₺{fin.kalan_odeme?.toLocaleString()}</td>
                  <td className="py-3 px-4">
                    <StatusBadge status={fin.durum} />
                  </td>
                  <td className="py-3 px-4 text-sm text-gray-500 max-w-[200px] truncate">
                    {fin.notlar || '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {finances.length === 0 && (
            <div className="p-8 text-center text-gray-500">Finans kaydı bulunmuyor.</div>
          )}
        </div>
      )}
    </div>
  );
};

export default Finance;
