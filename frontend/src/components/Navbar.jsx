import React from 'react';
import { 
  LayoutDashboard, Search, ListFilter, Sliders, 
  Activity, DollarSign, History, Settings as SettingsIcon, Play, Zap, Store
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, onSelectDemoScenario }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'analyzer', label: 'Transaction Analyzer', icon: Search },
    { id: 'queue', label: 'Review Queue', icon: ListFilter },
    { id: 'simulator', label: 'What-If Simulator', icon: Sliders },
    { id: 'model', label: 'Model Health', icon: Activity },
    { id: 'costs', label: 'Cost Analysis', icon: DollarSign },
    { id: 'audit', label: 'Audit Trail', icon: History },
    { id: 'settings', label: 'Settings', icon: SettingsIcon },
  ];

  const demoScenarios = [
    { id: 1, title: 'Scenario 1: Low-Risk Loyal (UPI)' },
    { id: 2, title: 'Scenario 2: Medium-Risk COD (Verify)' },
    { id: 3, title: 'Scenario 3: High-Risk Multi-Account (RTO)' },
    { id: 4, title: 'Scenario 4: High-Value COD Burst' },
    { id: 5, title: 'Scenario 5: False-Positive Candidate (Card)' },
  ];

  return (
    <header className="border-b border-[#1B3558] bg-[#0C2340] sticky top-0 z-50 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="w-9 h-9 rounded-lg bg-[#0066FF] flex items-center justify-center shadow-md shadow-[#0066FF]/30 border border-blue-400/40">
              <Zap className="w-5 h-5 text-white fill-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-xl tracking-tight text-white font-sans">
                  Razor<span className="text-[#3395FF]">Shield</span>
                </span>
                <span className="bg-[#0066FF]/20 text-[#479AFF] text-[10px] px-2 py-0.5 rounded font-bold uppercase tracking-wider border border-[#0066FF]/30">
                  AI Risk Manager
                </span>
              </div>
              <p className="text-[11px] text-slate-300 font-medium hidden sm:block">
                Built for Razorpay AI Buildathon • Detect. Explain. Decide. Prevent.
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <div className="hidden lg:flex items-center space-x-2 bg-[#07162A] border border-[#1B3558] rounded-lg py-1 px-2.5 text-xs text-slate-300">
              <Store className="w-3.5 h-3.5 text-[#3395FF]" />
              <span className="text-slate-400">Merchant:</span>
              <span className="text-white font-semibold font-mono">MERCH_001</span>
              <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#00B368] opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-[#00B368]"></span>
              </span>
            </div>

            <div className="flex items-center space-x-2 bg-[#07162A] border border-[#0066FF]/40 rounded-lg p-1.5 px-3 shadow-inner">
              <Play className="w-3.5 h-3.5 text-[#3395FF] fill-[#3395FF]/30" />
              <span className="text-xs text-slate-300 font-semibold hidden md:inline">Demo Scenarios:</span>
              <select
                className="bg-transparent text-xs text-white font-semibold outline-none cursor-pointer hover:text-[#3395FF]"
                onChange={(e) => {
                  const val = parseInt(e.target.value);
                  if (val && onSelectDemoScenario) onSelectDemoScenario(val);
                }}
                defaultValue=""
              >
                <option value="" disabled className="bg-[#0C2340] text-slate-400">Select Presentation Demo...</option>
                {demoScenarios.map(s => (
                  <option key={s.id} value={s.id} className="bg-[#0C2340] text-slate-100">
                    {s.title}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="flex space-x-1 overflow-x-auto py-2 border-t border-[#162D4A] no-scrollbar">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-md text-xs font-bold whitespace-nowrap transition-all ${
                  isActive
                    ? 'bg-[#0066FF] text-white shadow-sm shadow-[#0066FF]/25'
                    : 'text-slate-300 hover:text-white hover:bg-[#132E52] border border-transparent'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}
