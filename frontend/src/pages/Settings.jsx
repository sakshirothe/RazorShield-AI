import React, { useEffect, useState } from 'react';
import { Save, RefreshCw, CheckCircle, Sliders } from 'lucide-react';
import { getSettings, updateSettings } from '../services/api';

export default function Settings() {
  const [settings, setSettings] = useState({
    low_threshold: 30,
    medium_threshold: 70,
    verification_cost: 25.0,
    manual_review_cost: 65.0,
    false_positive_cost: 220.0,
    average_loss_per_risky_order: 2400.0,
    auto_approve_low_risk: true
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const res = await getSettings();
        setSettings(res);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      await updateSettings(settings);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (e) {
      alert(e.message);
    } finally {
      setSaving(false);
    }
  };

  const updateField = (field, val) => {
    setSettings(prev => ({
      ...prev,
      [field]: typeof prev[field] === 'boolean' ? val : parseFloat(val) || 0
    }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <RefreshCw className="w-6 h-6 text-[#0066FF] animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight">Merchant Risk Policy Settings</h1>
        <p className="text-xs text-slate-300 mt-1 font-normal">
          Configure risk thresholds and business cost coefficients.
          RazorShield adjusts dynamically to your margin tolerances and verification budgets.
        </p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5 space-y-4 shadow-sm">
          <div className="flex items-center space-x-2 pb-3 border-b border-[#1B3558]">
            <Sliders className="w-4 h-4 text-[#3395FF]" />
            <h2 className="text-xs font-extrabold text-white uppercase tracking-wider">
              Risk Level Threshold Boundaries (0 - 100 Scale)
            </h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-300 font-bold mb-1">
                Low-to-Medium Risk Cutoff
              </label>
              <input
                type="number"
                min="5"
                max="50"
                value={settings.low_threshold}
                onChange={e => updateField('low_threshold', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF]"
              />
              <span className="text-[10px] text-slate-400 block mt-1">
                0 to {settings.low_threshold}: Categorized as LOW (Seamless Approval)
              </span>
            </div>

            <div>
              <label className="block text-slate-300 font-bold mb-1">
                Medium-to-High Risk Cutoff
              </label>
              <input
                type="number"
                min="51"
                max="90"
                value={settings.medium_threshold}
                onChange={e => updateField('medium_threshold', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF]"
              />
              <span className="text-[10px] text-slate-400 block mt-1">
                {settings.low_threshold + 1} to {settings.medium_threshold}: MEDIUM • &gt;{settings.medium_threshold}: HIGH (Manual Review)
              </span>
            </div>
          </div>
        </div>

        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5 space-y-4 shadow-sm">
          <h2 className="text-xs font-extrabold text-white uppercase tracking-wider pb-3 border-b border-[#1B3558]">
            Financial & Operational Cost Parameters (in INR)
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-300 font-bold mb-1">
                Average Loss per RTO Incident (₹)
              </label>
              <input
                type="number"
                value={settings.average_loss_per_risky_order}
                onChange={e => updateField('average_loss_per_risky_order', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF]"
              />
              <span className="text-[10px] text-slate-400 block mt-1">Forward + reverse courier fees + restocking</span>
            </div>

            <div>
              <label className="block text-slate-300 font-bold mb-1">
                Automated Verification Cost (₹)
              </label>
              <input
                type="number"
                value={settings.verification_cost}
                onChange={e => updateField('verification_cost', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF]"
              />
              <span className="text-[10px] text-slate-400 block mt-1">SMS / WhatsApp OTP / IVR confirmation</span>
            </div>

            <div>
              <label className="block text-slate-300 font-bold mb-1">
                Manual Human Review Cost (₹)
              </label>
              <input
                type="number"
                value={settings.manual_review_cost}
                onChange={e => updateField('manual_review_cost', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF]"
              />
              <span className="text-[10px] text-slate-400 block mt-1">Fraud analyst processing time</span>
            </div>

            <div>
              <label className="block text-slate-300 font-bold mb-1">
                False-Positive Friction Cost (₹)
              </label>
              <input
                type="number"
                value={settings.false_positive_cost}
                onChange={e => updateField('false_positive_cost', e.target.value)}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF]"
              />
              <span className="text-[10px] text-slate-400 block mt-1">Customer delay / cart drop penalty</span>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between pt-2">
          {savedSuccess ? (
            <span className="text-xs text-[#00B368] font-bold flex items-center">
              <CheckCircle className="w-4 h-4 mr-1.5" />
              Settings successfully saved and active in decision engine!
            </span>
          ) : <span />}

          <button
            type="submit"
            disabled={saving}
            className="px-6 py-2.5 bg-[#0066FF] hover:bg-[#0052CC] text-white text-xs font-extrabold rounded-lg shadow-md shadow-[#0066FF]/30 flex items-center space-x-2 transition-all"
          >
            {saving ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
            <span>SAVE MERCHANT POLICY</span>
          </button>
        </div>
      </form>
    </div>
  );
}
