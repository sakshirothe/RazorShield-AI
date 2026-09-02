import React, { useState } from 'react';
import { HelpCircle, Sliders } from 'lucide-react';

export default function CostAnalysis() {
  const [assumptions, setAssumptions] = useState({
    avgLossPerRto: 2400,
    verificationCost: 25,
    manualReviewCost: 65,
    falsePositiveFriction: 220,
    testSetPositives: 736,
    testSetNegatives: 6764,
    testSetTruePositives: 489,
    testSetFalsePositives: 729,
    testSetFalseNegatives: 247
  });

  const updateAssumption = (field, val) => {
    setAssumptions(prev => ({
      ...prev,
      [field]: parseFloat(val) || 0
    }));
  };

  const costWithoutAi = assumptions.testSetPositives * assumptions.avgLossPerRto;
  const avoidedLoss = assumptions.testSetTruePositives * assumptions.avgLossPerRto;
  const fnCost = assumptions.testSetFalseNegatives * assumptions.avgLossPerRto;
  const fpCost = assumptions.testSetFalsePositives * assumptions.falsePositiveFriction;
  const interventionCost = (assumptions.testSetTruePositives + assumptions.testSetFalsePositives) * assumptions.verificationCost;

  const costWithAi = fnCost + fpCost + interventionCost;
  const netPreventedLoss = Math.max(costWithoutAi - costWithAi, 0);
  const roi = netPreventedLoss / Math.max(interventionCost, 1);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight">Cost-Sensitive Financial Analysis</h1>
        <p className="text-xs text-slate-300 mt-1 font-normal">
          Quantifying the economic trade-off between avoided RTO logistics losses, verification expenses, and false-positive customer friction.
        </p>
      </div>

      <div className="bg-[#0066FF]/10 border border-[#0066FF]/30 rounded-xl p-4 flex items-start space-x-3 shadow-sm">
        <HelpCircle className="w-5 h-5 text-[#3395FF] shrink-0 mt-0.5" />
        <div className="text-xs text-slate-300 space-y-1">
          <span className="font-extrabold text-[#3395FF] block uppercase tracking-wide">
            Illustrative Estimate Based on Configurable Business Assumptions
          </span>
          <p className="font-normal leading-relaxed">
            Metrics below contrast baseline financial loss (approving all transactions without defense) versus
            deploying RazorShield's AI intervention engine on the 7,500 held-out test cohort.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-[#0B1E36] border border-[#FF334B]/40 rounded-xl p-5 relative overflow-hidden shadow-sm">
          <div className="text-xs font-extrabold text-[#FF334B] uppercase tracking-wider mb-2">
            Status Quo (Without AI)
          </div>
          <div className="text-3xl font-black font-mono text-white">
            ₹{costWithoutAi.toLocaleString('en-IN')}
          </div>
          <p className="text-xs text-slate-300 mt-2 font-normal">
            Total unmitigated logistics loss across {assumptions.testSetPositives} doorstep rejections.
          </p>
          <div className="mt-4 pt-3 border-t border-[#1B3558] text-[11px] text-slate-400 space-y-1">
            <div className="flex justify-between">
              <span>Unmitigated RTO Orders:</span>
              <span className="font-mono text-white font-bold">{assumptions.testSetPositives}</span>
            </div>
            <div className="flex justify-between">
              <span>Average Loss per Incident:</span>
              <span className="font-mono text-white font-bold">₹{assumptions.avgLossPerRto}</span>
            </div>
          </div>
        </div>

        <div className="bg-[#0B1E36] border border-[#0066FF]/40 rounded-xl p-5 relative overflow-hidden shadow-sm">
          <div className="text-xs font-extrabold text-[#3395FF] uppercase tracking-wider mb-2">
            RazorShield (With AI)
          </div>
          <div className="text-3xl font-black font-mono text-white">
            ₹{costWithAi.toLocaleString('en-IN')}
          </div>
          <p className="text-xs text-slate-300 mt-2 font-normal">
            Sum of residual false negatives, verification costs, and customer friction.
          </p>
          <div className="mt-4 pt-3 border-t border-[#1B3558] text-[11px] text-slate-400 space-y-1">
            <div className="flex justify-between">
              <span>Verification Cost Incurred:</span>
              <span className="font-mono text-white font-bold">₹{interventionCost.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span>False-Positive Friction Cost:</span>
              <span className="font-mono text-white font-bold">₹{fpCost.toLocaleString()}</span>
            </div>
          </div>
        </div>

        <div className="bg-[#0B1E36] border border-[#00B368]/50 rounded-xl p-5 relative overflow-hidden shadow-md shadow-[#00B368]/10">
          <div className="text-xs font-extrabold text-[#00B368] uppercase tracking-wider mb-2 flex items-center justify-between">
            <span>Net Prevented Merchant Loss</span>
            <span className="px-2 py-0.5 rounded bg-[#00B368]/20 text-[#00B368] text-[10px] font-mono font-extrabold">
              {roi.toFixed(1)}x ROI
            </span>
          </div>
          <div className="text-3xl font-black font-mono text-[#00B368]">
            ₹{netPreventedLoss.toLocaleString('en-IN')}
          </div>
          <p className="text-xs text-slate-200 mt-2 font-normal">
            True net economic savings returned to merchant margin.
          </p>
          <div className="mt-4 pt-3 border-t border-[#1B3558] text-[11px] text-slate-400 space-y-1">
            <div className="flex justify-between">
              <span>Avoided Direct Losses:</span>
              <span className="font-mono text-[#00B368] font-bold">₹{avoidedLoss.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span>Net Margin Protection:</span>
              <span className="font-mono text-[#00B368] font-bold">+{((netPreventedLoss / costWithoutAi) * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5 space-y-4 shadow-sm">
        <div className="flex items-center space-x-2 pb-3 border-b border-[#1B3558]">
          <Sliders className="w-4 h-4 text-[#3395FF]" />
          <h2 className="text-xs font-extrabold text-white uppercase tracking-wider">
            Merchant Business Assumptions
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          <div>
            <label className="block text-slate-300 font-bold mb-1">Avg RTO Loss per Incident (₹)</label>
            <input
              type="number"
              value={assumptions.avgLossPerRto}
              onChange={e => updateAssumption('avgLossPerRto', e.target.value)}
              className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF]"
            />
            <span className="text-[10px] text-slate-400 block mt-1">Forward + reverse courier fees</span>
          </div>

          <div>
            <label className="block text-slate-300 font-bold mb-1">Verification Cost per Order (₹)</label>
            <input
              type="number"
              value={assumptions.verificationCost}
              onChange={e => updateAssumption('verificationCost', e.target.value)}
              className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF]"
            />
            <span className="text-[10px] text-slate-400 block mt-1">WhatsApp / SMS OTP fee</span>
          </div>

          <div>
            <label className="block text-slate-300 font-bold mb-1">Manual Review Cost (₹)</label>
            <input
              type="number"
              value={assumptions.manualReviewCost}
              onChange={e => updateAssumption('manualReviewCost', e.target.value)}
              className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF]"
            />
            <span className="text-[10px] text-slate-400 block mt-1">Analyst processing expense</span>
          </div>

          <div>
            <label className="block text-slate-300 font-bold mb-1">False-Positive Friction Cost (₹)</label>
            <input
              type="number"
              value={assumptions.falsePositiveFriction}
              onChange={e => updateAssumption('falsePositiveFriction', e.target.value)}
              className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-white font-mono font-bold outline-none focus:border-[#0066FF]"
            />
            <span className="text-[10px] text-slate-400 block mt-1">Customer cart drop penalty</span>
          </div>
        </div>
      </div>
    </div>
  );
}
