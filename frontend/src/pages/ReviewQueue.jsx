import React, { useState, useEffect } from 'react';
import { 
  RefreshCw, UserCheck
} from 'lucide-react';
import { getReviews, submitReviewDecision } from '../services/api';

export default function ReviewQueue() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState('ALL');
  const [selectedReview, setSelectedReview] = useState(null);

  const [overrideAction, setOverrideAction] = useState('APPROVED');
  const [overrideReason, setOverrideReason] = useState('Customer confirmed order identity via OTP / Phone call');
  const [submitting, setSubmitting] = useState(false);

  const fetchReviews = async () => {
    try {
      setLoading(true);
      const params = filterStatus === 'ALL' ? {} : { status: filterStatus };
      const res = await getReviews(params);
      setReviews(res.items || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReviews();
  }, [filterStatus]);

  const handleDecision = async () => {
    if (!selectedReview) return;
    try {
      setSubmitting(true);
      await submitReviewDecision(selectedReview.id, {
        action: overrideAction,
        reason: overrideReason,
        operator_name: 'Merchant Risk Specialist'
      });
      setSelectedReview(null);
      fetchReviews();
    } catch (err) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">Risk Review Queue</h1>
          <p className="text-xs text-slate-300 mt-1 font-normal">
            Human-in-the-Loop decision gateway. Review flagged orders and record auditable human overrides.
          </p>
        </div>

        <div className="flex items-center space-x-1.5 bg-[#07162A] border border-[#1B3558] p-1 rounded-lg overflow-x-auto">
          {['ALL', 'PENDING', 'APPROVED', 'VERIFICATION_REQUIRED', 'MANUAL_REVIEW'].map((st) => (
            <button
              key={st}
              onClick={() => setFilterStatus(st)}
              className={`px-3 py-1 rounded-md text-xs font-bold whitespace-nowrap transition-all ${
                filterStatus === st
                  ? 'bg-[#0066FF] text-white shadow-sm shadow-[#0066FF]/20'
                  : 'text-slate-400 hover:text-white hover:bg-[#132E52]'
              }`}
            >
              {st.replace(/_/g, ' ')}
            </button>
          ))}
        </div>
      </div>

      <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl overflow-hidden shadow-sm">
        {loading ? (
          <div className="p-12 text-center text-slate-400 text-xs flex items-center justify-center space-x-2">
            <RefreshCw className="w-4 h-4 animate-spin text-[#0066FF]" />
            <span className="font-semibold">Loading flagged transactions...</span>
          </div>
        ) : reviews.length === 0 ? (
          <div className="p-12 text-center text-slate-400 text-xs">
            No transactions found for status <span className="font-mono text-white font-bold">{filterStatus}</span>.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#07162A] border-b border-[#1B3558] text-slate-400 uppercase tracking-wider font-extrabold text-[10px]">
                <tr>
                  <th className="py-3 px-4">Transaction Reference</th>
                  <th className="py-3 px-4">Amount</th>
                  <th className="py-3 px-4">Risk Score</th>
                  <th className="py-3 px-4">Risk Level</th>
                  <th className="py-3 px-4">Primary Trigger</th>
                  <th className="py-3 px-4">AI Recommendation</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1B3558]/60 font-medium">
                {reviews.map((r) => (
                  <tr key={r.id} className="hover:bg-[#07162A]/50 transition-all">
                    <td className="py-3 px-4 font-mono font-bold text-white">
                      {r.transaction_id}
                      <span className="block text-[10px] text-slate-400 font-normal font-sans">{r.customer_id}</span>
                    </td>
                    <td className="py-3 px-4 font-mono font-extrabold text-slate-100">
                      ₹{r.order_value.toLocaleString('en-IN')}
                    </td>
                    <td className="py-3 px-4 font-mono font-extrabold">
                      <span className={
                        r.risk_score >= 70 ? 'text-[#FF334B]' :
                        r.risk_score >= 30 ? 'text-[#FF8800]' : 'text-[#00B368]'
                      }>
                        {r.risk_score}/100
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`inline-flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] font-bold ${
                        r.risk_level === 'HIGH' ? 'bg-[#FF334B]/15 text-[#FF334B] border border-[#FF334B]/30' :
                        r.risk_level === 'MEDIUM' ? 'bg-[#FF8800]/15 text-[#FF8800] border border-[#FF8800]/30' :
                        'bg-[#00B368]/15 text-[#00B368] border border-[#00B368]/30'
                      }`}>
                        <span className={`w-1.5 h-1.5 rounded-full ${
                          r.risk_level === 'HIGH' ? 'bg-[#FF334B]' :
                          r.risk_level === 'MEDIUM' ? 'bg-[#FF8800]' : 'bg-[#00B368]'
                        }`} />
                        <span>{r.risk_level}</span>
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-300 font-normal">
                      {r.top_risk_factor || 'Threshold Exceeded'}
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-200 font-bold">
                      {r.recommended_action}
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        r.status === 'PENDING' ? 'bg-[#FF8800]/20 text-[#FF8800]' :
                        r.status === 'APPROVED' ? 'bg-[#00B368]/20 text-[#00B368]' :
                        r.status === 'REJECTED' ? 'bg-[#FF334B]/20 text-[#FF334B]' :
                        'bg-[#0066FF]/20 text-[#479AFF]'
                      }`}>
                        {r.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => setSelectedReview(r)}
                        className="px-3 py-1 bg-[#0066FF] hover:bg-[#0052CC] text-white text-xs font-bold rounded-md shadow-sm transition-all"
                      >
                        Override / Decide
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {selectedReview && (
        <div className="fixed inset-0 bg-black/75 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0C2340] border border-[#1B3558] rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-[#1B3558]">
              <div className="flex items-center space-x-2">
                <UserCheck className="w-5 h-5 text-[#3395FF]" />
                <h3 className="text-sm font-bold text-white font-sans">Human Operator Override</h3>
              </div>
              <button 
                onClick={() => setSelectedReview(null)}
                className="text-slate-400 hover:text-white text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <div className="bg-[#07162A] p-3 rounded-lg border border-[#1B3558] text-xs space-y-1 font-mono">
              <div className="flex justify-between">
                <span className="text-slate-400 font-sans">Order ID:</span>
                <span className="text-white font-bold">{selectedReview.transaction_id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 font-sans">Amount:</span>
                <span className="text-white font-bold">₹{selectedReview.order_value.toLocaleString('en-IN')}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 font-sans">AI Recommendation:</span>
                <span className="text-[#FF8800] font-bold">{selectedReview.recommended_action}</span>
              </div>
            </div>

            <div>
              <label className="text-xs text-slate-300 font-bold block mb-1.5">
                Select Final Business Action
              </label>
              <div className="grid grid-cols-3 gap-2 text-xs">
                <button
                  type="button"
                  onClick={() => setOverrideAction('APPROVED')}
                  className={`py-2 px-3 rounded-lg font-bold border transition-all ${
                    overrideAction === 'APPROVED'
                      ? 'bg-[#00B368] text-white border-[#00B368]'
                      : 'bg-[#07162A] text-slate-300 border-[#1B3558] hover:text-white'
                  }`}
                >
                  Approve
                </button>
                <button
                  type="button"
                  onClick={() => setOverrideAction('VERIFICATION_REQUESTED')}
                  className={`py-2 px-3 rounded-lg font-bold border transition-all ${
                    overrideAction === 'VERIFICATION_REQUESTED'
                      ? 'bg-[#FF8800] text-black border-[#FF8800]'
                      : 'bg-[#07162A] text-slate-300 border-[#1B3558] hover:text-white'
                  }`}
                >
                  Request OTP
                </button>
                <button
                  type="button"
                  onClick={() => setOverrideAction('REJECTED')}
                  className={`py-2 px-3 rounded-lg font-bold border transition-all ${
                    overrideAction === 'REJECTED'
                      ? 'bg-[#FF334B] text-white border-[#FF334B]'
                      : 'bg-[#07162A] text-slate-300 border-[#1B3558] hover:text-white'
                  }`}
                >
                  Reject
                </button>
              </div>
            </div>

            <div>
              <label className="text-xs text-slate-300 font-bold block mb-1">
                Audit Reason (Logged to Immutable Audit Trail)
              </label>
              <textarea
                value={overrideReason}
                onChange={e => setOverrideReason(e.target.value)}
                rows={3}
                className="w-full bg-[#07162A] border border-[#1B3558] rounded-lg p-2.5 text-xs text-white outline-none focus:border-[#0066FF] font-normal"
                placeholder="Specify justification for approval or rejection..."
              />
            </div>

            <div className="flex items-center justify-end space-x-2 pt-2 border-t border-[#1B3558]">
              <button
                type="button"
                onClick={() => setSelectedReview(null)}
                className="px-4 py-2 bg-[#07162A] text-slate-300 rounded-lg text-xs font-bold hover:bg-slate-800 border border-[#1B3558]"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleDecision}
                disabled={submitting}
                className="px-4 py-2 bg-[#0066FF] hover:bg-[#0052CC] text-white rounded-lg text-xs font-bold shadow-md shadow-[#0066FF]/30"
              >
                {submitting ? 'Recording...' : 'Confirm Decision & Log Audit'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
