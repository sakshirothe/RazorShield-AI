import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import TransactionAnalyzer from './pages/TransactionAnalyzer';
import ReviewQueue from './pages/ReviewQueue';
import WhatIfSimulator from './pages/WhatIfSimulator';
import ModelPerformance from './pages/ModelPerformance';
import CostAnalysis from './pages/CostAnalysis';
import AuditLog from './pages/AuditLog';
import Settings from './pages/Settings';

const PRESET_SCENARIOS = {
  1: {
    order_value: 1499.0,
    payment_method: 'UPI',
    product_category: 'Fashion & Apparel',
    quantity: 1,
    account_age_days: 420,
    previous_orders: 24,
    previous_returns: 1,
    previous_refunds: 1,
    previous_rto_count: 0,
    days_since_last_order: 12,
    orders_last_7_days: 1,
    orders_last_30_days: 3,
    address_change_count: 0,
    device_account_count: 1,
    shipping_distance_km: 180.0,
    pincode_risk_score: 0.12,
    delivery_attempts: 0,
    payment_failure_count: 0
  },
  2: {
    order_value: 2899.0,
    payment_method: 'COD',
    product_category: 'Footwear',
    quantity: 1,
    account_age_days: 65,
    previous_orders: 4,
    previous_returns: 1,
    previous_refunds: 1,
    previous_rto_count: 0,
    days_since_last_order: 28,
    orders_last_7_days: 1,
    orders_last_30_days: 2,
    address_change_count: 1,
    device_account_count: 1,
    shipping_distance_km: 650.0,
    pincode_risk_score: 0.45,
    delivery_attempts: 1,
    payment_failure_count: 1
  },
  3: {
    order_value: 6499.0,
    payment_method: 'COD',
    product_category: 'Electronics',
    quantity: 2,
    account_age_days: 4,
    previous_orders: 3,
    previous_returns: 2,
    previous_refunds: 2,
    previous_rto_count: 2,
    days_since_last_order: 2,
    orders_last_7_days: 4,
    orders_last_30_days: 4,
    address_change_count: 3,
    device_account_count: 4,
    shipping_distance_km: 1600.0,
    pincode_risk_score: 0.78,
    delivery_attempts: 2,
    payment_failure_count: 2
  },
  4: {
    order_value: 18500.0,
    payment_method: 'COD',
    product_category: 'Jewelry & Accessories',
    quantity: 3,
    account_age_days: 2,
    previous_orders: 0,
    previous_returns: 0,
    previous_refunds: 0,
    previous_rto_count: 0,
    days_since_last_order: 2,
    orders_last_7_days: 5,
    orders_last_30_days: 5,
    address_change_count: 2,
    device_account_count: 3,
    shipping_distance_km: 2100.0,
    pincode_risk_score: 0.82,
    delivery_attempts: 0,
    payment_failure_count: 2
  },
  5: {
    order_value: 12000.0,
    payment_method: 'CREDIT_CARD',
    product_category: 'Electronics',
    quantity: 1,
    account_age_days: 18,
    previous_orders: 1,
    previous_returns: 0,
    previous_refunds: 0,
    previous_rto_count: 0,
    days_since_last_order: 14,
    orders_last_7_days: 1,
    orders_last_30_days: 1,
    address_change_count: 1,
    device_account_count: 1,
    shipping_distance_km: 1400.0,
    pincode_risk_score: 0.55,
    delivery_attempts: 0,
    payment_failure_count: 0
  }
};

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentScenario, setCurrentScenario] = useState(null);

  const handleSelectDemoScenario = (scenarioId) => {
    const sc = PRESET_SCENARIOS[scenarioId];
    if (sc) {
      setCurrentScenario(sc);
      setActiveTab('analyzer');
    }
  };

  return (
    <div className="min-h-screen bg-[#061325] text-slate-100 flex flex-col selection:bg-[#0066FF] selection:text-white font-sans">
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        onSelectDemoScenario={handleSelectDemoScenario}
      />

      <main className="flex-1 p-4 sm:p-6 lg:p-8">
        {activeTab === 'dashboard' && (
          <Dashboard setActiveTab={setActiveTab} />
        )}
        {activeTab === 'analyzer' && (
          <TransactionAnalyzer 
            key={JSON.stringify(currentScenario)} 
            initialScenario={currentScenario}
            setActiveTab={setActiveTab}
          />
        )}
        {activeTab === 'queue' && <ReviewQueue />}
        {activeTab === 'simulator' && <WhatIfSimulator />}
        {activeTab === 'model' && <ModelPerformance />}
        {activeTab === 'costs' && <CostAnalysis />}
        {activeTab === 'audit' && <AuditLog />}
        {activeTab === 'settings' && <Settings />}
      </main>

      <footer className="border-t border-[#1B3558] bg-[#0C2340] py-4 px-6 text-center text-xs text-slate-400">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center space-x-2">
            <span className="font-extrabold text-white">Razor<span className="text-[#3395FF]">Shield</span></span>
            <span className="text-slate-500">•</span>
            <span>Cost-Sensitive AI Risk Manager for RTO & Return Abuse</span>
          </div>
          <div>
            Built for the <span className="text-[#3395FF] font-extrabold">Razorpay AI Buildathon</span> (AI Risk Manager Track)
          </div>
        </div>
      </footer>
    </div>
  );
}
