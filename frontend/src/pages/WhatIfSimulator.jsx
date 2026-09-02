import React, { useState, useEffect } from 'react';
import { AlertCircle, Sparkles } from 'lucide-react';
import { simulateRisk } from '../services/api';

export default function WhatIfSimulator() {
  const [params, setParams] = useState({
    order_value: 7500,
    payment_method: 'COD',
    account_age_days: 10,
    previous_orders: 5,
    previous_returns: 3,
    previous_rto_count: 2,
    address_change_count: 2,
    device_account_count: 3,
    pincode_risk_score: 0.75,
    shipping_distance_km: 1200
  });

  const [simResult, setSimResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const runSim = async (currentParams) => {
    try {
      setLoading(true);
      const res = await simulateRisk(currentParams);
      setSimResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runSim(params);
  }, [params]);

  const updateParam = (field, val) => {
    setParams(prev => ({
      ...prev,
      [field]: field === 'payment_method' ? val : parseFloat(val) || 0
    }));
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="bg-[#FF8800]/10 border border-[#FF8800]/30 rounded-xl p-4 flex items-center justify-between shadow-sm">
        <div className="flex items-center space-x-3">
          <AlertCircle className="w-5 h-5 text-[#FF8800] shrink-0" />
          <div>
            <span className="text-xs font-extrabold text-[#FF8800] uppercase tracking-wider">
              What-If Risk Sensitivity Simulator
            </span>
            <p className="text-xs text-slate-300 mt-0.5 font-normal">
              This is an interactive model simulation, not a persisted historical transaction. 
              Adjust sliders below to observe how checkout parameter shifts alter AI risk predictions in real-time.
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-6 bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5 space-y-5 shadow-sm">
          <h2 className="text-xs font-extrabold text-white uppercase tracking-wider pb-3 border-b border-[#1B3558]">
            Simulated Checkout Parameters
          </h2>

          <div>
            <label className="text-xs font-bold text-slate-300 block mb-1.5">
              Payment Method
            </label>
            <div className="grid grid-cols-3 gap-2">
              {['COD', 'UPI', 'CREDIT_CARD'].map(pm => (
                <button
                  key={pm}
                  onClick={() => updateParam('payment_method', pm)}
                  className={`py-2 text-xs font-bold rounded-lg border transition-all ${
                    params.payment_method === pm
                      ? 'bg-[#0066FF] text-white border-[#0066FF] shadow-sm shadow-[#0066FF]/30'
                      : 'bg-[#07162A] text-slate-400 border-[#1B3558] hover:text-white'
                  }`}
                >
                  {pm}
                </button>
              ))}
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1.5 font-bold">
              <span className="text-slate-300">Order Ticket Value (INR)</span>
              <span className="font-mono text-[#3395FF]">₹{params.order_value.toLocaleString()}</span>
            </div>
            <input
              type="range"
              min="500"
              max="25000"
              step="500"
              value={params.order_value}
              onChange={e => updateParam('order_value', e.target.value)}
              className="w-full h-1.5 bg-[#07162A] rounded-lg appearance-none cursor-pointer accent-[#0066FF]"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1.5 font-bold">
              <span className="text-slate-300">Customer Account Age (Days)</span>
              <span className="font-mono text-[#3395FF]">{params.account_age_days} days</span>
            </div>
            <input
              type="range"
              min="1"
              max="700"
              step="5"
              value={params.account_age_days}
              onChange={e => updateParam('account_age_days', e.target.value)}
              className="w-full h-1.5 bg-[#07162A] rounded-lg appearance-none cursor-pointer accent-[#0066FF]"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1.5 font-bold">
              <span className="text-slate-300">Previous Returned Orders</span>
              <span className="font-mono text-[#3395FF]">{params.previous_returns} items</span>
            </div>
            <input
              type="range"
              min="0"
              max="15"
              step="1"
              value={params.previous_returns}
              onChange={e => updateParam('previous_returns', e.target.value)}
              className="w-full h-1.5 bg-[#07162A] rounded-lg appearance-none cursor-pointer accent-[#0066FF]"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1.5 font-bold">
              <span className="text-slate-300">Device Fingerprint Sharing</span>
              <span className="font-mono text-[#3395FF]">{params.device_account_count} accounts</span>
            </div>
            <input
              type="range"
              min="1"
              max="8"
              step="1"
              value={params.device_account_count}
              onChange={e => updateParam('device_account_count', e.target.value)}
              className="w-full h-1.5 bg-[#07162A] rounded-lg appearance-none cursor-pointer accent-[#0066FF]"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1.5 font-bold">
              <span className="text-slate-300">Address Modifications on Record</span>
              <span className="font-mono text-[#3395FF]">{params.address_change_count} changes</span>
            </div>
            <input
              type="range"
              min="0"
              max="6"
              step="1"
              value={params.address_change_count}
              onChange={e => updateParam('address_change_count', e.target.value)}
              className="w-full h-1.5 bg-[#07162A] rounded-lg appearance-none cursor-pointer accent-[#0066FF]"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1.5 font-bold">
              <span className="text-slate-300">Pincode Logistics Risk Index</span>
              <span className="font-mono text-[#3395FF]">{params.pincode_risk_score}</span>
            </div>
            <input
              type="range"
              min="0.05"
              max="0.95"
              step="0.05"
              value={params.pincode_risk_score}
              onChange={e => updateParam('pincode_risk_score', e.target.value)}
              className="w-full h-1.5 bg-[#07162A] rounded-lg appearance-none cursor-pointer accent-[#0066FF]"
            />
          </div>
        </div>

        <div className="lg:col-span-6 space-y-4">
          {simResult && (
            <div className="space-y-4">
              <div className={`p-6 rounded-xl border ${
                simResult.decision.risk_level === 'HIGH' ? 'bg-[#FF334B]/10 border-[#FF334B]/40' :
                simResult.decision.risk_level === 'MEDIUM' ? 'bg-[#FF8800]/10 border-[#FF8800]/40' :
                'bg-[#00B368]/10 border-[#00B368]/40'
              }`}>
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">
                      Simulated Risk Category
                    </span>
                    <div className="text-2xl font-black text-white mt-1">
                      {simResult.decision.risk_level} RISK
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-4xl font-extrabold font-mono text-white">
                      {simResult.decision.risk_score}
                    </span>
                    <span className="text-sm text-slate-400"> / 100</span>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-white/10 flex items-center justify-between">
                  <span className="text-xs font-extrabold text-white">
                    Action: {simResult.decision.recommended_action.replace(/_/g, ' ')}
                  </span>
                  <span className="text-xs text-[#00B368] font-mono font-bold">
                    Net Benefit: ₹{simResult.decision.expected_benefit.toLocaleString()}
                  </span>
                </div>
              </div>

              <div className="bg-[#0B1E36] border border-[#0066FF]/40 rounded-xl p-4 shadow-md shadow-[#0066FF]/5">
                <div className="flex items-center space-x-2 text-[#3395FF] text-xs font-bold uppercase mb-2">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Simulation Reasoning</span>
                </div>
                <p className="text-xs text-slate-200 leading-relaxed font-sans font-normal">
                  {simResult.ai_risk_assessment}
                </p>
              </div>

              <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-4">
                <h3 className="text-xs font-extrabold text-white uppercase tracking-wider mb-3 pb-2 border-b border-[#1B3558]">
                  Sensitivity Drivers
                </h3>
                <div className="space-y-2">
                  {simResult.top_risk_factors.slice(0, 4).map((f, idx) => (
                    <div key={idx} className="p-2 bg-[#07162A] border border-[#1B3558] rounded-lg text-xs flex justify-between">
                      <span className="text-slate-300 font-medium">{f.feature_name}</span>
                      <span className="font-mono text-[#FF334B] font-bold">+{f.contribution}</span>
                    </div>
                  ))}
                  {simResult.top_protective_factors.slice(0, 2).map((f, idx) => (
                    <div key={idx} className="p-2 bg-[#07162A] border border-[#1B3558] rounded-lg text-xs flex justify-between">
                      <span className="text-slate-300 font-medium">{f.feature_name}</span>
                      <span className="font-mono text-[#00B368] font-bold">{f.contribution}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
