import React, { useState } from 'react';
import { 
  Search, 
  Sparkles, Activity, Zap 
} from 'lucide-react';
import { analyzeTransaction } from '../services/api';

export default function TransactionAnalyzer({ initialScenario = null, setActiveTab }) {
  const defaultPayload = {
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
  };

  const [form, setForm] = useState(initialScenario || defaultPayload);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (field, val) => {
    setForm(prev => ({
      ...prev,
      [field]: ['payment_method', 'product_category'].includes(field) ? val : parseFloat(val) || 0
    }));
  };

  const runAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await analyzeTransaction(form);
      setResult(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight">Transaction Risk Analyzer</h1>
        <p className="text-xs text-slate-300 mt-1 font-normal">
          Real-time risk scoring using calibrated LightGBM, Tree SHAP factor attribution, and cost-sensitive economic decision logic.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-5 bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5 space-y-4 shadow-sm">
          <div className="flex items-center justify-between pb-3 border-b border-[#1B3558]">
            <h2 className="text-xs font-extrabold text-white uppercase tracking-wider">Order & Customer Profile</h2>
            <span className="text-[10px] text-[#479AFF] font-mono font-bold bg-[#0066FF]/15 px-2 py-0.5 rounded border border-[#0066FF]/30">
              Live Inspector
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Order Value (₹)</label>
              <input 
                type="number" 
                value={form.order_value} 
                onChange={e => handleInputChange('order_value', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF] transition-all"
              />
            </div>
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Payment Method</label>
              <select 
                value={form.payment_method} 
                onChange={e => handleInputChange('payment_method', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-bold outline-none focus:border-[#0066FF] transition-all cursor-pointer"
              >
                <option value="COD">COD (Cash on Delivery)</option>
                <option value="UPI">UPI (Instant Prepaid)</option>
                <option value="CREDIT_CARD">Credit Card</option>
                <option value="DEBIT_CARD">Debit Card</option>
                <option value="NET_BANKING">Net Banking</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Product Category</label>
              <select 
                value={form.product_category} 
                onChange={e => handleInputChange('product_category', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-bold outline-none focus:border-[#0066FF] transition-all cursor-pointer"
              >
                <option value="Electronics">Electronics</option>
                <option value="Fashion & Apparel">Fashion & Apparel</option>
                <option value="Footwear">Footwear</option>
                <option value="Beauty & Personal Care">Beauty & Personal Care</option>
                <option value="Jewelry & Accessories">Jewelry & Accessories</option>
                <option value="Home & Kitchen">Home & Kitchen</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Account Age (Days)</label>
              <input 
                type="number" 
                value={form.account_age_days} 
                onChange={e => handleInputChange('account_age_days', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF] transition-all"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-2 text-xs">
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Prior Orders</label>
              <input 
                type="number" 
                value={form.previous_orders} 
                onChange={e => handleInputChange('previous_orders', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2 text-white font-mono font-bold outline-none focus:border-[#0066FF] transition-all"
              />
            </div>
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Past Returns</label>
              <input 
                type="number" 
                value={form.previous_returns} 
                onChange={e => handleInputChange('previous_returns', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2 text-white font-mono font-bold outline-none focus:border-[#0066FF] transition-all"
              />
            </div>
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Past RTOs</label>
              <input 
                type="number" 
                value={form.previous_rto_count} 
                onChange={e => handleInputChange('previous_rto_count', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2 text-white font-mono font-bold outline-none focus:border-[#0066FF] transition-all"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Device Multi-Accounts</label>
              <input 
                type="number" 
                value={form.device_account_count} 
                onChange={e => handleInputChange('device_account_count', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF] transition-all"
              />
            </div>
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Address Changes</label>
              <input 
                type="number" 
                value={form.address_change_count} 
                onChange={e => handleInputChange('address_change_count', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF] transition-all"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Pincode Risk Score</label>
              <input 
                type="number" 
                step="0.05" 
                value={form.pincode_risk_score} 
                onChange={e => handleInputChange('pincode_risk_score', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF] transition-all"
              />
            </div>
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Shipping Transit (km)</label>
              <input 
                type="number" 
                value={form.shipping_distance_km} 
                onChange={e => handleInputChange('shipping_distance_km', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF] transition-all"
              />
            </div>
          </div>

          <button
            onClick={runAnalysis}
            disabled={loading}
            className="w-full py-3 bg-[#0066FF] hover:bg-[#0052CC] text-white font-extrabold text-xs rounded-lg shadow-md shadow-[#0066FF]/30 transition-all flex items-center justify-center space-x-2"
          >
            {loading ? (
              <Activity className="w-4 h-4 animate-spin" />
            ) : (
              <>
                <Zap className="w-4 h-4 fill-white" />
                <span>EVALUATE RISK & DECISION</span>
              </>
            )}
          </button>
        </div>

        <div className="lg:col-span-7 space-y-4">
          {error && (
            <div className="p-4 bg-[#FF334B]/10 border border-[#FF334B]/30 rounded-xl text-xs text-[#FF334B] font-semibold">
              {error}
            </div>
          )}

          {!result && !loading && (
            <div className="bg-[#0B1E36] border border-[#1B3558] border-dashed rounded-xl p-12 text-center flex flex-col items-center justify-center min-h-[420px]">
              <div className="w-12 h-12 rounded-xl bg-[#07162A] border border-[#1B3558] flex items-center justify-center mb-3">
                <Search className="w-6 h-6 text-[#3395FF]" />
              </div>
              <h3 className="text-sm font-bold text-white">Ready for Analysis</h3>
              <p className="text-xs text-slate-400 max-w-sm mt-1">
                Configure attributes on the left or select a preset demo scenario above, then click Evaluate Risk.
              </p>
            </div>
          )}

          {result && (
            <div className="space-y-4">
              <div className={`p-5 rounded-xl border ${
                result.decision.risk_level === 'HIGH' 
                  ? 'bg-[#FF334B]/10 border-[#FF334B]/40 text-slate-100' :
                result.decision.risk_level === 'MEDIUM' 
                  ? 'bg-[#FF8800]/10 border-[#FF8800]/40 text-slate-100' :
                  'bg-[#00B368]/10 border-[#00B368]/40 text-slate-100'
              }`}>
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider ${
                        result.decision.risk_level === 'HIGH' ? 'bg-[#FF334B] text-white' :
                        result.decision.risk_level === 'MEDIUM' ? 'bg-[#FF8800] text-black' :
                        'bg-[#00B368] text-white'
                      }`}>
                        {result.decision.risk_level} RISK
                      </span>
                      <span className="text-xs font-mono font-extrabold px-2 py-0.5 rounded bg-[#07162A] text-white border border-[#1B3558]">
                        Score: {result.decision.risk_score} / 100
                      </span>
                    </div>
                    <div className="text-lg font-extrabold text-white mt-1.5 font-sans">
                      ACTION: {result.decision.recommended_action.replace(/_/g, ' ')}
                    </div>
                  </div>

                  <div className="text-right sm:text-right">
                    <div className="text-[10px] text-slate-400 uppercase font-semibold">Transaction ID</div>
                    <div className="text-xs font-mono text-[#3395FF] font-bold">{result.transaction_id}</div>
                  </div>
                </div>

                <p className="text-xs text-slate-300 mt-3 pt-3 border-t border-white/10 leading-relaxed font-normal">
                  {result.decision.reason}
                </p>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-3.5 shadow-sm">
                  <span className="text-[10px] text-slate-400 font-semibold uppercase block">Potential Loss</span>
                  <span className="text-lg font-extrabold font-mono text-white mt-0.5 block">
                    ₹{result.decision.estimated_loss.toLocaleString('en-IN')}
                  </span>
                  <span className="text-[10px] text-slate-400 block mt-0.5">Courier & packaging</span>
                </div>
                <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-3.5 shadow-sm">
                  <span className="text-[10px] text-slate-400 font-semibold uppercase block">Intervention Cost</span>
                  <span className="text-lg font-extrabold font-mono text-white mt-0.5 block">
                    ₹{result.decision.intervention_cost.toLocaleString('en-IN')}
                  </span>
                  <span className="text-[10px] text-slate-400 block mt-0.5">OTP / Analyst time</span>
                </div>
                <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-3.5 shadow-sm">
                  <span className="text-[10px] text-[#00B368] font-semibold uppercase block">Net Expected ROI</span>
                  <span className="text-lg font-extrabold font-mono text-[#00B368] mt-0.5 block">
                    ₹{result.decision.expected_benefit.toLocaleString('en-IN')}
                  </span>
                  <span className="text-[10px] text-emerald-400/80 block mt-0.5">Avoided loss minus cost</span>
                </div>
              </div>

              <div className="bg-[#0B1E36] border border-[#0066FF]/40 rounded-xl p-4 shadow-md shadow-[#0066FF]/5">
                <div className="flex items-center space-x-2 text-[#3395FF] text-xs font-bold uppercase tracking-wider mb-2">
                  <Sparkles className="w-4 h-4 text-[#3395FF]" />
                  <span>AI Risk Manager Operational Narrative (Grounded Fact Synthesis)</span>
                </div>
                <p className="text-xs text-slate-200 leading-relaxed font-sans font-normal">
                  {result.ai_risk_assessment}
                </p>
              </div>

              <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-4">
                <div className="flex items-center justify-between mb-3 pb-2 border-b border-[#1B3558]">
                  <h3 className="text-xs font-extrabold text-white uppercase tracking-wider">
                    Tree SHAP Contributing Factors
                  </h3>
                  <span className="text-[10px] text-slate-400 italic">
                    {result.metadata.disclaimer}
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <h4 className="text-[11px] font-bold text-[#FF334B] mb-2 flex items-center">
                      <span className="w-2 h-2 rounded-full bg-[#FF334B] mr-1.5" />
                      Risk-Increasing Factors (+)
                    </h4>
                    <div className="space-y-1.5">
                      {result.top_risk_factors.map((factor, idx) => (
                        <div key={idx} className="p-2 rounded-lg bg-[#07162A] border border-[#1B3558] text-[11px] flex items-center justify-between">
                          <span className="text-slate-300 font-medium">{factor.feature_name}</span>
                          <span className="font-mono text-[#FF334B] font-bold">+{factor.contribution}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="text-[11px] font-bold text-[#00B368] mb-2 flex items-center">
                      <span className="w-2 h-2 rounded-full bg-[#00B368] mr-1.5" />
                      Protective Buffers (-)
                    </h4>
                    <div className="space-y-1.5">
                      {result.top_protective_factors.map((factor, idx) => (
                        <div key={idx} className="p-2 rounded-lg bg-[#07162A] border border-[#1B3558] text-[11px] flex items-center justify-between">
                          <span className="text-slate-300 font-medium">{factor.feature_name}</span>
                          <span className="font-mono text-[#00B368] font-bold">{factor.contribution}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
