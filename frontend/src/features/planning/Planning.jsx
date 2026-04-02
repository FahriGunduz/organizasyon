import React, { useState, useEffect } from 'react';
import api from '../../api/axios';
import { Calendar, Plus, Save, UserPlus, FileText } from 'lucide-react';

const Planning = () => {
  const [customers, setCustomers] = useState([]);
  const [events, setEvents] = useState([]);
  
  // Tab State
  const [activeTab, setActiveTab] = useState('events'); // events, new-event, new-customer

  // Form States
  const [customerForm, setCustomerForm] = useState({ ad: '', soyad: '', telefon: '', firma_turu: 'Bireysel' });
  const [eventForm, setEventForm] = useState({ etkinlik_adi: '', musteri_id: '', tarih: '', mekan: '', sorumlu_firma: 'La Vita Bella' });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [cusRes, evtRes] = await Promise.all([
        api.get('/planning/customers'),
        api.get('/planning/events')
      ]);
      setCustomers(cusRes.data);
      setEvents(evtRes.data);
      if (cusRes.data.length > 0) {
        setEventForm(prev => ({ ...prev, musteri_id: cusRes.data[0].id }));
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleCustomerSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/planning/customers', customerForm);
      alert('Müşteri eklendi!');
      fetchData();
      setCustomerForm({ ad: '', soyad: '', telefon: '', firma_turu: 'Bireysel' });
      setActiveTab('new-event');
    } catch (err) {
      alert('Hata: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleEventSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/planning/events', {
        ...eventForm,
        musteri_id: Number(eventForm.musteri_id)
      });
      alert('Etkinlik başarıyla oluşturuldu!');
      fetchData();
      setEventForm({ ...eventForm, etkinlik_adi: '', mekan: '' });
      setActiveTab('events');
    } catch (err) {
      alert('Hata: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-primary-DEFAULT">Etkinlik Planlama</h1>
        <div className="flex gap-2">
          <button 
            onClick={() => setActiveTab('new-customer')}
            className={`px-3 py-1.5 rounded-lg font-medium text-sm transition-colors flex items-center gap-1 ${activeTab === 'new-customer' ? 'bg-primary-DEFAULT text-white' : 'bg-white text-gray-600 border'}`}>
            <UserPlus className="w-4 h-4" /> Müşteri Ekle
          </button>
          <button 
            onClick={() => setActiveTab('new-event')}
            className={`px-3 py-1.5 rounded-lg font-medium text-sm transition-colors flex items-center gap-1 ${activeTab === 'new-event' ? 'bg-accent-DEFAULT text-white' : 'bg-white text-gray-600 border'}`}>
            <Plus className="w-4 h-4" /> Yeni Etkinlik
          </button>
          <button 
            onClick={() => setActiveTab('events')}
            className={`px-3 py-1.5 rounded-lg font-medium text-sm transition-colors flex items-center gap-1 ${activeTab === 'events' ? 'bg-primary-DEFAULT text-white' : 'bg-white text-gray-600 border'}`}>
            <Calendar className="w-4 h-4" /> Takvim/Liste
          </button>
        </div>
      </div>

      {activeTab === 'events' && (
        <div className="card p-6">
          <h2 className="text-lg font-semibold mb-4 border-b pb-2">Tüm Etkinlikler</h2>
          {events.length === 0 ? <p className="text-gray-500 text-sm">Henüz etkinlik bulunmuyor.</p> : (
            <div className="grid gap-4">
              {events.map(ev => (
                <div key={ev.id} className="border p-4 rounded-lg flex flex-col md:flex-row justify-between md:items-center gap-4 bg-gray-50 hover:bg-white transition-colors border-l-4 border-l-accent-DEFAULT">
                  <div>
                    <h3 className="font-bold text-primary-DEFAULT">{ev.etkinlik_adi}</h3>
                    <p className="text-sm text-gray-600 flex items-center gap-1 mt-1">
                      <Calendar className="w-3.5 h-3.5"/> {ev.tarih} | {ev.mekan}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">Müşteri: {ev.musteri_adi} | Firma: {ev.sorumlu_firma}</p>
                  </div>
                  <div className="flex flex-col items-end">
                    <span className="bg-primary-light text-white text-xs px-2 py-1 rounded">{ev.durum}</span>
                    <span className="text-xs text-gray-500 mt-2">Ekipman Onayı: %{ev.ilerleme_yuzdesi}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'new-customer' && (
        <div className="card p-6 max-w-2xl mx-auto">
          <h2 className="text-lg font-semibold mb-4 border-b pb-2 flex items-center gap-2"><UserPlus className="w-5 h-5"/> Yeni Müşteri Ekle</h2>
          <form onSubmit={handleCustomerSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-600 mb-1">Ad <span className="text-red-500">*</span></label>
                <input required className="input-field" type="text" value={customerForm.ad} onChange={e => setCustomerForm({...customerForm, ad: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Soyad <span className="text-red-500">*</span></label>
                <input required className="input-field" type="text" value={customerForm.soyad} onChange={e => setCustomerForm({...customerForm, soyad: e.target.value})} />
              </div>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Telefon <span className="text-red-500">*</span></label>
              <input required className="input-field" type="tel" value={customerForm.telefon} onChange={e => setCustomerForm({...customerForm, telefon: e.target.value})} />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Firma / Bireysel</label>
              <select className="input-field" value={customerForm.firma_turu} onChange={e => setCustomerForm({...customerForm, firma_turu: e.target.value})}>
                <option value="Bireysel">Bireysel Aile/Müşteri</option>
                <option value="Kurumsal">Kurumsal Şirket</option>
              </select>
            </div>
            <button type="submit" className="btn-primary w-full mt-4 flex items-center justify-center gap-2"><Save className="w-4 h-4"/> Müşteriyi Kaydet</button>
          </form>
        </div>
      )}

      {activeTab === 'new-event' && (
        <div className="card p-6 max-w-2xl mx-auto">
          <h2 className="text-lg font-semibold mb-4 border-b pb-2 flex items-center gap-2"><FileText className="w-5 h-5"/> Yeni Etkinlik Oluştur</h2>
          <form onSubmit={handleEventSubmit} className="space-y-4">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Seçili Müşteri <span className="text-red-500">*</span></label>
              <select required className="input-field" value={eventForm.musteri_id} onChange={e => setEventForm({...eventForm, musteri_id: e.target.value})}>
                <option value="" disabled>Müşteri Seçin</option>
                {customers.map(c => <option key={c.id} value={c.id}>{c.ad} {c.soyad} ({c.telefon})</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Etkinlik Adı <span className="text-red-500">*</span></label>
              <input required placeholder="Örn: Yılmaz & Demir Düğünü" className="input-field" type="text" value={eventForm.etkinlik_adi} onChange={e => setEventForm({...eventForm, etkinlik_adi: e.target.value})} />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-600 mb-1">Tarih <span className="text-red-500">*</span></label>
                <input required className="input-field" type="date" value={eventForm.tarih} onChange={e => setEventForm({...eventForm, tarih: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Sorumlu Firma</label>
                <select className="input-field" value={eventForm.sorumlu_firma} onChange={e => setEventForm({...eventForm, sorumlu_firma: e.target.value})}>
                  <option value="La Vita Bella">La Vita Bella</option>
                  <option value="Umut Aybar">Umut Aybar Organizasyon</option>
                  <option value="Ortak">Ortak Operasyon</option>
                </select>
              </div>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Mekan / Otel <span className="text-red-500">*</span></label>
              <input required placeholder="Etkinliğin yapılacağı mekan adresi" className="input-field" type="text" value={eventForm.mekan} onChange={e => setEventForm({...eventForm, mekan: e.target.value})} />
            </div>
            <button type="submit" className="btn-accent w-full mt-4 flex items-center justify-center gap-2"><Save className="w-4 h-4"/> Etkinliği Onayla ve Oluştur</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default Planning;
