import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Layers, CalendarDays, Wallet, QrCode } from 'lucide-react';
import clsx from 'clsx';

const Navbar = () => {
  const location = useLocation();

  const navLinks = [
    { name: 'Dashboard', path: '/', icon: <Layers className="w-5 h-5 mr-1" /> },
    { name: 'Planlama', path: '/planning', icon: <CalendarDays className="w-5 h-5 mr-1" /> },
    { name: 'Finans', path: '/finance', icon: <Wallet className="w-5 h-5 mr-1" /> },
    { name: 'QR Saha', path: '/qr-scanner', icon: <QrCode className="w-5 h-5 mr-1" />, isHighlight: true }
  ];

  return (
    <nav className="bg-primary-DEFAULT text-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center gap-2">
              <div className="bg-accent-DEFAULT p-1.5 rounded-lg">
                <Layers className="w-6 h-6 text-primary-DEFAULT" />
              </div>
              <span className="font-bold text-xl tracking-wide">EOS</span>
            </Link>
          </div>
          
          {/* Desktop Nav */}
          <div className="hidden md:flex items-center space-x-6">
            {navLinks.map((link) => (
              <Link
                key={link.name}
                to={link.path}
                className={clsx(
                  "flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer",
                  location.pathname === link.path 
                    ? "bg-primary-light text-accent-DEFAULT" 
                    : "text-gray-300 hover:bg-primary-light hover:text-white",
                  link.isHighlight && "border border-accent-DEFAULT text-accent-DEFAULT"
                )}
              >
                {link.icon}
                {link.name}
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Mobile Nav Sticky Bottom (Mobile-first QR focus) */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-primary-DEFAULT shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] border-t border-primary-light z-50">
        <div className="flex justify-around items-center h-16 pb-safe">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              to={link.path}
              className={clsx(
                "flex flex-col items-center justify-center w-full h-full text-xs font-medium transition-colors",
                location.pathname === link.path 
                  ? "text-accent-DEFAULT" 
                  : "text-gray-400 hover:text-white",
                link.isHighlight && "text-accent-light"
              )}
            >
              <div className={clsx("mb-1", link.isHighlight && "bg-accent-DEFAULT/20 p-2 rounded-full")}>
                {link.icon}
              </div>
              <span className="truncate max-w-[80px]">{link.name}</span>
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
