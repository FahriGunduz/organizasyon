import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './features/dashboard/Dashboard';
import QRScanner from './features/inventory/QRScanner';
import Planning from './features/planning/Planning';
import Finance from './features/finance/Finance';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/qr-scanner" element={<QRScanner />} />
          <Route path="/planning" element={<Planning />} />
          <Route path="/finance" element={<Finance />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
