import React from 'react';
import clsx from 'clsx';
import { Package, Truck, Tent, CheckCircle, Clock } from 'lucide-react';

export const STATUS_MAP = {
  "Planlandı": { color: "bg-gray-100 text-gray-700 border-gray-200", icon: Clock },
  "Aktif": { color: "bg-blue-100 text-blue-700 border-blue-200", icon: Clock },
  "Tamamlandı": { color: "bg-green-100 text-green-700 border-green-200", icon: CheckCircle },
  "İptal": { color: "bg-red-100 text-red-700 border-red-200", icon: Clock },
  "Hazırlandı": { color: "bg-orange-100 text-orange-700 border-orange-200", icon: Package },
  "Yüklendi": { color: "bg-amber-100 text-amber-700 border-amber-200", icon: Truck },
  "Kuruldu": { color: "bg-blue-100 text-blue-700 border-blue-200", icon: Tent },
  "Toplandı": { color: "bg-emerald-100 text-emerald-700 border-emerald-200", icon: CheckCircle },
  "Bekliyor": { color: "bg-gray-100 text-gray-700 border-gray-200", icon: Clock },
  "Kısmi Ödeme": { color: "bg-amber-100 text-amber-700 border-amber-200", icon: Clock },
};

const StatusBadge = ({ status, className }) => {
  const config = STATUS_MAP[status] || { color: "bg-gray-100 text-gray-700 border-gray-200", icon: Clock };
  const Icon = config.icon;

  return (
    <span className={clsx(
      "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border",
      config.color,
      className
    )}>
      <Icon className="w-3.5 h-3.5" />
      {status}
    </span>
  );
};

export default StatusBadge;
