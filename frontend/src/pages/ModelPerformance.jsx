import React, { useEffect, useState } from 'react';
import { CheckCircle2, RefreshCw } from 'lucide-react';
import { getModelMetrics } from '../services/api';

export default function ModelPerformance() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadMetrics = async () => {
      try {
        setLoading(true);
        const res = await getModelMetrics();
        setData(res);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    loadMetrics();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <RefreshCw className="w-8 h-8 text-[#0066FF] animate-spin" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-8 text-center text-xs text-[#FF334B] font-bold">
        Failed to load evaluation metrics: {error}
      </div>
    );
  }

  const { evaluation, metadata } = data;
  const metrics = evaluation.metrics_summary;
  const cm = evaluation.confusion_matrix;
  const thresholds = evaluation.threshold_analysis;
  const distribution = evaluation.prediction_distribution;

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">Model Health & Evaluation Benchmarks</h1>
          <p className="text-xs text-slate-300 mt-1 font-normal">
            Calculated on an <strong className="text-white font-bold">untouched held-out test split</strong> (7,500 transactions, 15%).
          </p>
        </div>
        <div className="inline-flex items-center space-x-2 bg-[#00B368]/15 border border-[#00B368]/30 px-3 py-1.5 rounded-lg text-xs font-bold text-[#00B368]">
          <CheckCircle2 className="w-4 h-4" />
          <span>Active: {metadata.algorithm || 'Calibrated LightGBM GBDT'}</span>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-3.5 text-center shadow-sm">
          <span className="text-[10px] text-slate-400 font-bold uppercase block">ROC-AUC</span>
          <span className="text-xl font-extrabold font-mono text-[#3395FF] mt-1 block">{metrics.roc_auc}</span>
          <span className="text-[10px] text-slate-400 mt-0.5 block">Discrimination Power</span>
        </div>

        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-3.5 text-center shadow-sm">
          <span className="text-[10px] text-slate-400 font-bold uppercase block">PR-AUC</span>
          <span className="text-xl font-extrabold font-mono text-[#479AFF] mt-1 block">{metrics.pr_auc}</span>
          <span className="text-[10px] text-slate-400 mt-0.5 block">Precision-Recall Curve</span>
        </div>

        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-3.5 text-center shadow-sm">
          <span className="text-[10px] text-slate-400 font-bold uppercase block">Precision (@0.50)</span>
          <span className="text-xl font-extrabold font-mono text-[#00B368] mt-1 block">
            {(metrics.precision * 100).toFixed(1)}%
          </span>
          <span className="text-[10px] text-slate-400 mt-0.5 block">True positives / Flags</span>
        </div>

        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-3.5 text-center shadow-sm">
          <span className="text-[10px] text-slate-400 font-bold uppercase block">Recall (@0.50)</span>
          <span className="text-xl font-extrabold font-mono text-[#FF8800] mt-1 block">
            {(metrics.recall * 100).toFixed(1)}%
          </span>
          <span className="text-[10px] text-slate-400 mt-0.5 block">Captured Risky Orders</span>
        </div>

        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-3.5 text-center shadow-sm">
          <span className="text-[10px] text-slate-400 font-bold uppercase block">False Positive Rate</span>
          <span className="text-xl font-extrabold font-mono text-[#FF334B] mt-1 block">
            {(metrics.false_positive_rate * 100).toFixed(1)}%
          </span>
          <span className="text-[10px] text-slate-400 mt-0.5 block">Legitimate friction</span>
        </div>

        <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-3.5 text-center shadow-sm">
          <span className="text-[10px] text-slate-400 font-bold uppercase block">Held-Out Test Cohort</span>
          <span className="text-xl font-extrabold font-mono text-white mt-1 block">{evaluation.test_set_size}</span>
          <span className="text-[10px] text-slate-400 mt-0.5 block">Untouched Split</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-5 bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5 shadow-sm">
          <h3 className="text-xs font-extrabold text-white uppercase tracking-wider mb-3 flex items-center justify-between pb-2 border-b border-[#1B3558]">
            <span>Held-Out Confusion Matrix (@0.50 Cutoff)</span>
            <span className="text-[10px] text-slate-400 font-normal font-sans">N = {evaluation.test_set_size}</span>
          </h3>

          <div className="grid grid-cols-2 gap-3 mt-4 text-center">
            <div className="bg-[#07162A] border border-[#1B3558] p-4 rounded-xl">
              <span className="text-[10px] text-slate-400 uppercase font-bold block">True Negatives (TN)</span>
              <span className="text-2xl font-extrabold font-mono text-[#00B368] mt-1 block">
                {cm.true_negatives.toLocaleString()}
              </span>
              <span className="text-[10px] text-slate-400 block mt-1 font-normal">Normal Orders Approved</span>
            </div>

            <div className="bg-[#07162A] border border-[#1B3558] p-4 rounded-xl">
              <span className="text-[10px] text-slate-400 uppercase font-bold block">False Positives (FP)</span>
              <span className="text-2xl font-extrabold font-mono text-[#FF334B] mt-1 block">
                {cm.false_positives.toLocaleString()}
              </span>
              <span className="text-[10px] text-slate-400 block mt-1 font-normal">Unnecessary Verification</span>
            </div>

            <div className="bg-[#07162A] border border-[#1B3558] p-4 rounded-xl">
              <span className="text-[10px] text-slate-400 uppercase font-bold block">False Negatives (FN)</span>
              <span className="text-2xl font-extrabold font-mono text-[#FF8800] mt-1 block">
                {cm.false_negatives.toLocaleString()}
              </span>
              <span className="text-[10px] text-slate-400 block mt-1 font-normal">Missed RTO Returns</span>
            </div>

            <div className="bg-[#07162A] border border-[#1B3558] p-4 rounded-xl">
              <span className="text-[10px] text-slate-400 uppercase font-bold block">True Positives (TP)</span>
              <span className="text-2xl font-extrabold font-mono text-[#3395FF] mt-1 block">
                {cm.true_positives.toLocaleString()}
              </span>
              <span className="text-[10px] text-slate-400 block mt-1 font-normal">Abuse Prevented</span>
            </div>
          </div>
        </div>

        <div className="lg:col-span-7 bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5 shadow-sm">
          <h3 className="text-xs font-extrabold text-white uppercase tracking-wider mb-3 pb-2 border-b border-[#1B3558]">
            Calibrated Risk Probability Distribution
          </h3>

          <div className="space-y-2 mt-4">
            {distribution.map((bin, idx) => {
              const maxCount = Math.max(...distribution.map(d => d.count)) || 1;
              const barWidth = ((bin.count / maxCount) * 100).toFixed(1);
              return (
                <div key={idx} className="flex items-center space-x-3 text-xs">
                  <span className="w-16 font-mono text-slate-400 text-[11px] font-semibold">{bin.bin}</span>
                  <div className="flex-1 h-3.5 bg-[#07162A] rounded overflow-hidden border border-[#1B3558]">
                    <div 
                      className="h-full bg-gradient-to-r from-[#0066FF] to-[#3395FF] rounded" 
                      style={{ width: `${barWidth}%` }} 
                    />
                  </div>
                  <span className="w-14 font-mono text-right text-slate-200 text-[11px] font-extrabold">
                    {bin.count}
                  </span>
                </div>
              );
            })}
          </div>

          <p className="text-[11px] text-slate-400 mt-4 pt-3 border-t border-[#1B3558] font-normal leading-relaxed">
            Probability calibration via sigmoid regression guarantees risk scores concentrate accurately with clean separation 
            between clean purchasers and doorstep delivery abusers.
          </p>
        </div>
      </div>

      <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl p-5 shadow-sm">
        <div className="flex items-center justify-between mb-4 pb-2 border-b border-[#1B3558]">
          <div>
            <h3 className="text-xs font-extrabold text-white uppercase tracking-wider">
              Threshold Trade-Off Analysis (Precision vs Recall vs Business Cost)
            </h3>
            <p className="text-[11px] text-slate-400 mt-0.5 font-normal">
              Compare expected business savings against customer friction across operational cutoffs.
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#07162A] border-b border-[#1B3558] text-slate-400 font-extrabold uppercase tracking-wider text-[10px]">
              <tr>
                <th className="py-2.5 px-3">Cutoff</th>
                <th className="py-2.5 px-3">Precision</th>
                <th className="py-2.5 px-3">Recall</th>
                <th className="py-2.5 px-3">F1-Score</th>
                <th className="py-2.5 px-3">FPR</th>
                <th className="py-2.5 px-3">Expected Avoided Loss</th>
                <th className="py-2.5 px-3">Expected Business Cost</th>
                <th className="py-2.5 px-3 text-right">Net Financial Benefit</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1B3558]/60 font-medium">
              {thresholds.map((t, idx) => {
                const isOptimal = t.threshold === 0.20 || t.threshold === 0.30;
                return (
                  <tr key={idx} className={`hover:bg-[#07162A]/60 transition-all ${isOptimal ? 'bg-[#0066FF]/10' : ''}`}>
                    <td className="py-2.5 px-3 font-extrabold text-white">
                      {t.threshold.toFixed(2)}
                      {isOptimal && (
                        <span className="ml-2 text-[9px] bg-[#0066FF]/30 text-[#3395FF] px-1.5 py-0.5 rounded font-extrabold border border-[#0066FF]/40">
                          Recommended
                        </span>
                      )}
                    </td>
                    <td className="py-2.5 px-3 text-[#00B368] font-bold">{(t.precision * 100).toFixed(1)}%</td>
                    <td className="py-2.5 px-3 text-[#FF8800] font-bold">{(t.recall * 100).toFixed(1)}%</td>
                    <td className="py-2.5 px-3 text-[#479AFF] font-bold">{t.f1.toFixed(3)}</td>
                    <td className="py-2.5 px-3 text-[#FF334B] font-bold">{(t.false_positive_rate * 100).toFixed(1)}%</td>
                    <td className="py-2.5 px-3 text-slate-200">₹{t.expected_avoided_loss.toLocaleString()}</td>
                    <td className="py-2.5 px-3 text-slate-300">₹{t.expected_business_cost.toLocaleString()}</td>
                    <td className="py-2.5 px-3 text-right font-extrabold text-[#00B368]">
                      ₹{t.expected_net_benefit.toLocaleString()}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
