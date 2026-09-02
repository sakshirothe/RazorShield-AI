import React, { useEffect, useState } from 'react';
import { 
  ShieldAlert, ShieldCheck, TrendingUp, AlertTriangle, 
  ArrowUpRight, RefreshCw, ChevronRight, CheckCircle2, Zap
} from 'lucide-react';
import { getDashboard } from '../services/api';

export default function Dashboard({ setActiveTab, onSelectTransaction }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchSummary = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getDashboard();
      setData(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center space-y-3">
          <RefreshCw className="w-8 h-8 text-[#0066FF] animate-spin" />
          <p className="text-xs font-semibold text-slate-300">Loading risk telemetry...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 max-w-4xl mx-auto">
        <div className="bg-[#FF334B]/10 border border-[#FF334B]/30 rounded-xl p-6 text-center">
          <AlertTriangle className="w-10 h-10 text-[#FF334B] mx-auto mb-2" />
          <h3 className="text-base font-bold text-white">Connection Error</h3>
          <p className="text-xs text-slate-300 mt-1">{error}</p>
          <button 
            onClick={fetchSummary}
            className="mt-4 px-4 py-2 bg-[#0066FF] hover:bg-[#0052CC] text-xs font-bold rounded-lg text-white transition-all shadow-sm"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  const { overview, risk_distribution, category_breakdown, payment_breakdown } = data;

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="bg-gradient-to-r from-[#0C2340] via-[#0F2A4E] to-[#0C2340] border border-[#1B3558] rounded-xl p-6 relative overflow-hidden shadow-lg">
        <div className="absolute right-0 top-0 w-96 h-96 bg-[#0066FF]/10 rounded-full blur-3xl pointer-events-none" />
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="inline-flex items-center space-x-2 bg-[#0066FF]/20 border border-[#0066FF]/40 px-3 py-0.5 rounded-full text-xs font-bold text-[#479AFF] mb-2.5">
              <Zap className="w-3 h-3 fill-current text-[#479AFF]" />
              <span>Razorpay AI Buildathon — AI Risk Manager Track</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              RazorShield Risk Operations Center
            </h1>
            <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-2xl font-normal leading-relaxed">
              Cost-sensitive defense system detecting Return-to-Origin (RTO) and abusive returns, 
              explaining risk factors via Tree SHAP, and optimizing intervention ROI for merchants.
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setActiveTab('analyzer')}
              className="px-4 py-2.5 bg-[#0066FF] hover:bg-[#0052CC] text-white text-xs font-bold rounded-lg shadow-md shadow-[#0066FF]/30 transition-all flex items-center space-x-2"
            >
              <span>Analyze Order</span>
              <ChevronRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => setActiveTab('queue')}
              className="px-4 py-2.5 bg-[#07162A] hover:bg-[#132E52] border border-[#1B3558] text-slate-200 text-xs font-bold rounded-lg transition-all"
            >
              Review Queue ({overview.pending_reviews})
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5 hover:border-[#3395FF]/60 transition-all shadow-sm relative overflow-hidden">
          <div className="absolute top-0 left-0 right-0 h-1 bg-[#00B368]" />
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Prevented RTO Loss</span>
            <div className="w-8 h-8 rounded-lg bg-[#00B368]/15 flex items-center justify-center border border-[#00B368]/30">
              <ShieldCheck className="w-4 h-4 text-[#00B368]" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl sm:text-3xl font-extrabold text-white font-mono tracking-tight">
              ₹{overview.total_prevented_loss.toLocaleString('en-IN')}
            </div>
            <p className="text-[11px] text-[#00B368] mt-1.5 flex items-center font-semibold">
              <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" />
              <span>Optimized Margin Protection</span>
            </p>
          </div>
        </div>

        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5 hover:border-[#3395FF]/60 transition-all shadow-sm relative overflow-hidden">
          <div className="absolute top-0 left-0 right-0 h-1 bg-[#FF334B]" />
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">High-Risk Orders</span>
            <div className="w-8 h-8 rounded-lg bg-[#FF334B]/15 flex items-center justify-center border border-[#FF334B]/30">
              <ShieldAlert className="w-4 h-4 text-[#FF334B]" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl sm:text-3xl font-extrabold text-white font-mono tracking-tight">
              {overview.high_risk_count} <span className="text-xs font-normal text-slate-400 font-sans">flagged</span>
            </div>
            <p className="text-[11px] text-[#FF334B] mt-1.5 font-semibold">
              <span>Potential Loss: ₹{overview.total_estimated_loss.toLocaleString('en-IN')}</span>
            </p>
          </div>
        </div>

        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5 hover:border-[#3395FF]/60 transition-all shadow-sm relative overflow-hidden">
          <div className="absolute top-0 left-0 right-0 h-1 bg-[#FF8800]" />
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Verification Pool</span>
            <div className="w-8 h-8 rounded-lg bg-[#FF8800]/15 flex items-center justify-center border border-[#FF8800]/30">
              <AlertTriangle className="w-4 h-4 text-[#FF8800]" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl sm:text-3xl font-extrabold text-white font-mono tracking-tight">
              {overview.medium_risk_count} <span className="text-xs font-normal text-slate-400 font-sans">orders</span>
            </div>
            <p className="text-[11px] text-[#FF8800] mt-1.5 font-semibold">
              <span>WhatsApp / OTP verification</span>
            </p>
          </div>
        </div>

        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5 hover:border-[#3395FF]/60 transition-all shadow-sm relative overflow-hidden">
          <div className="absolute top-0 left-0 right-0 h-1 bg-[#0066FF]" />
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Seamless Approvals</span>
            <div className="w-8 h-8 rounded-lg bg-[#0066FF]/15 flex items-center justify-center border border-[#0066FF]/30">
              <CheckCircle2 className="w-4 h-4 text-[#479AFF]" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl sm:text-3xl font-extrabold text-white font-mono tracking-tight">
              {overview.low_risk_count} <span className="text-xs font-normal text-slate-400 font-sans">orders</span>
            </div>
            <p className="text-[11px] text-[#479AFF] mt-1.5 font-semibold">
              <span>Zero friction checkout</span>
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5">
          <h3 className="text-xs font-extrabold text-white uppercase tracking-wider mb-4 pb-2 border-b border-[#1B3558]">
            Risk Tier Distribution
          </h3>
          <div className="space-y-4">
            {risk_distribution.map((item, idx) => {
              const total = overview.total_transactions || 1;
              const pct = ((item.value / total) * 100).toFixed(1);
              const colorClass = idx === 0 ? '#00B368' : idx === 1 ? '#FF8800' : '#FF334B';
              return (
                <div key={idx} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-200 font-semibold">{item.name}</span>
                    <span className="text-slate-400 font-mono font-bold">{item.value} ({pct}%)</span>
                  </div>
                  <div className="w-full h-2 bg-[#07162A] rounded-full overflow-hidden">
                    <div 
                      className="h-full rounded-full transition-all duration-500" 
                      style={{ width: `${pct}%`, backgroundColor: colorClass }} 
                    />
                  </div>
                </div>
              );
            })}
          </div>

          <div className="mt-6 pt-4 border-t border-[#1B3558] text-[11px] text-slate-400 flex items-center justify-between">
            <span>Total Inspected Cohort:</span>
            <span className="font-mono font-bold text-white">{overview.total_transactions} orders</span>
          </div>
        </div>

        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5">
          <h3 className="text-xs font-extrabold text-white uppercase tracking-wider mb-4 pb-2 border-b border-[#1B3558]">
            Payment Method Risk Heatmap
          </h3>
          <div className="space-y-2.5">
            {payment_breakdown.map((pm, idx) => {
              const isCOD = pm.payment_method === 'COD';
              return (
                <div key={idx} className="p-3 bg-[#07162A] border border-[#1B3558] rounded-lg flex items-center justify-between hover:border-[#3395FF]/40 transition-all">
                  <div>
                    <div className="text-xs font-bold text-white flex items-center space-x-2">
                      <span>{pm.payment_method}</span>
                      {isCOD && (
                        <span className="text-[9px] bg-[#FF334B]/20 text-[#FF334B] px-1.5 py-0.2 rounded font-extrabold border border-[#FF334B]/40">
                          HIGH RTO
                        </span>
                      )}
                    </div>
                    <div className="text-[11px] text-slate-400 mt-0.5 font-mono">
                      {pm.total_orders} orders recorded
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-xs font-extrabold font-mono ${
                      pm.avg_risk_score > 60 ? 'text-[#FF334B]' :
                      pm.avg_risk_score > 30 ? 'text-[#FF8800]' : 'text-[#00B368]'
                    }`}>
                      Avg: {pm.avg_risk_score}/100
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5">
          <h3 className="text-xs font-extrabold text-white uppercase tracking-wider mb-4 pb-2 border-b border-[#1B3558]">
            Category Risk Exposure
          </h3>
          <div className="space-y-2.5">
            {category_breakdown.map((cat, idx) => (
              <div key={idx} className="p-3 bg-[#07162A] border border-[#1B3558] rounded-lg flex items-center justify-between hover:border-[#3395FF]/40 transition-all">
                <div>
                  <div className="text-xs font-bold text-white">{cat.category}</div>
                  <div className="text-[11px] text-slate-400 font-mono">
                    ₹{cat.total_amount.toLocaleString('en-IN')} vol
                  </div>
                </div>
                <div className="text-right">
                  <span className={`text-[10px] px-2 py-0.5 rounded font-mono font-bold ${
                    cat.avg_risk_score > 55 ? 'bg-[#FF334B]/15 text-[#FF334B] border border-[#FF334B]/30' :
                    cat.avg_risk_score > 30 ? 'bg-[#FF8800]/15 text-[#FF8800] border border-[#FF8800]/30' :
                    'bg-[#00B368]/15 text-[#00B368] border border-[#00B368]/30'
                  }`}>
                    {cat.avg_risk_score} score
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
