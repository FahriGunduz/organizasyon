import React, { useState, useEffect } from 'react';
import api from '../../api/axios';
import { Users, Package, Wallet, TrendingUp, Calendar, ArrowRight } from 'lucide-react';
import StatusBadge from '../../components/StatusBadge';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsRes, eventsRes] = await Promise.all([
          api.get('/dashboard/stats'),
          api.get('/planning/events')
        ]);
        setStats(statsRes.data);
        setEvents(eventsRes.data.slice(0, 5)); // Son 5 etkinlik
      } catch (err) {
        console.error("Dashboard data load error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) return <div className="text-center py-20 text-gray-500">Yükleniyor...</div>;

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-primary-DEFAULT">Ofis Panosu</h1>
          <p className="text-gray-500 mt-1">La Vita Bella & Umut Aybar Ortak Yönetim Sistemi</p>
        </div>
        <div className="flex bg-white px-4 py-2 rounded-lg shadow-sm border border-gray-100 gap-2 items-center">
          <Calendar className="w-5 h-5 text-accent-DEFAULT" />
          <span className="font-medium text-gray-700"> {new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' })}</span>
        </div>
      </div>

      {/* KPI Stats */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="card p-6 border-l-4 border-l-accent-DEFAULT">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm font-medium text-gray-500 mb-1">Aktif Etkinlikler</p>
                <h3 className="text-3xl font-bold text-gray-900">{stats.etkinlikler.aktif}</h3>
              </div>
              <div className="bg-orange-50 p-3 rounded-lg">
                <Calendar className="w-6 h-6 text-accent-DEFAULT" />
              </div>
            </div>
            <div className="mt-4 flex items-center text-sm">
              <span className="text-gray-500">Toplam {stats.etkinlikler.toplam} planlı</span>
            </div>
          </div>

          <div className="card p-6 border-l-4 border-l-blue-500">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm font-medium text-gray-500 mb-1">Kayıtlı Müşteri</p>
                <h3 className="text-3xl font-bold text-gray-900">{stats.musteriler}</h3>
              </div>
              <div className="bg-blue-50 p-3 rounded-lg">
                <Users className="w-6 h-6 text-blue-500" />
              </div>
            </div>
          </div>

          <div className="card p-6 border-l-4 border-l-emerald-500">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm font-medium text-gray-500 mb-1">Bekleyen Tahsilat</p>
                <h3 className="text-3xl font-bold text-gray-900">₺{stats.finans.bekleyen.toLocaleString('tr-TR')}</h3>
              </div>
              <div className="bg-emerald-50 p-3 rounded-lg">
                <Wallet className="w-6 h-6 text-emerald-500" />
              </div>
            </div>
            <div className="mt-4 flex items-center text-sm">
              <span className="text-green-600 font-medium">₺{stats.finans.tahsil_edilen.toLocaleString('tr-TR')} tahsil edildi</span>
            </div>
          </div>

          <div className="card p-6 border-l-4 border-l-purple-500">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm font-medium text-gray-500 mb-1">Operasyon İlerlemesi</p>
                <h3 className="text-3xl font-bold text-gray-900">%{stats.operasyon.ilerleme}</h3>
              </div>
              <div className="bg-purple-50 p-3 rounded-lg">
                <Package className="w-6 h-6 text-purple-500" />
              </div>
            </div>
            <div className="mt-4 w-full bg-gray-100 rounded-full h-1.5">
              <div className="bg-purple-500 h-1.5 rounded-full" style={{ width: `${stats.operasyon.ilerleme}%` }}></div>
            </div>
          </div>
        </div>
      )}

      {/* Recent Events List */}
      <div className="mt-8">
        <div className="flex justify-between items-end mb-4">
          <h2 className="text-xl font-bold text-primary-DEFAULT">Yaklaşan Etkinlikler</h2>
          <Link to="/planning" className="text-accent-DEFAULT hover:text-accent-dark flex items-center text-sm font-medium">
            Tümünü Gör <ArrowRight className="w-4 h-4 ml-1" />
          </Link>
        </div>
        
        <div className="card overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="py-3 px-4 font-semibold text-gray-600 text-sm">Etkinlik</th>
                <th className="py-3 px-4 font-semibold text-gray-600 text-sm">Müşteri</th>
                <th className="py-3 px-4 font-semibold text-gray-600 text-sm">Tarih</th>
                <th className="py-3 px-4 font-semibold text-gray-600 text-sm">Durum</th>
                <th className="py-3 px-4 font-semibold text-gray-600 text-sm">Sorumlu</th>
                <th className="py-3 px-4 font-semibold text-gray-600 text-sm">Ekipman</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {events.map((event) => (
                <tr key={event.id} className="hover:bg-gray-50 transition-colors">
                  <td className="py-3 px-4">
                    <div className="font-medium text-gray-900">{event.etkinlik_adi}</div>
                    <div className="text-xs text-gray-500">{event.mekan}</div>
                  </td>
                  <td className="py-3 px-4 text-sm text-gray-700">{event.musteri_adi}</td>
                  <td className="py-3 px-4 text-sm text-gray-700">
                    {new Date(event.tarih).toLocaleDateString('tr-TR')}
                  </td>
                  <td className="py-3 px-4">
                    <StatusBadge status={event.durum} />
                  </td>
                  <td className="py-3 px-4 text-sm font-medium text-gray-700">
                    {event.sorumlu_firma}
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                       <div className="w-full bg-gray-200 rounded-full h-1.5 w-16">
                          <div className="bg-accent-DEFAULT h-1.5 rounded-full" style={{ width: `${event.ilerleme_yuzdesi}%` }}></div>
                       </div>
                       <span className="text-xs text-gray-500">{event.tamamlanan_ekipman}/{event.toplam_ekipman}</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {events.length === 0 && (
            <div className="p-8 text-center text-gray-500">Kayıtlı etkinlik bulunmuyor.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
