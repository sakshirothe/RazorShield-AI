import React, { useEffect, useState } from 'react';
import { UserCheck, RefreshCw } from 'lucide-react';
import { getAuditLogs } from '../services/api';

export default function AuditLog() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [overrideFilter, setOverrideFilter] = useState(false);
  const [search, setSearch] = useState('');

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const params = { limit: 50 };
      if (overrideFilter) params.human_override_only = true;
      if (search) params.search = search;
      const res = await getAuditLogs(params);
      setLogs(res.items || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [overrideFilter]);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">Immutable Audit Trail</h1>
          <p className="text-xs text-slate-300 mt-1 font-normal">
            Complete chronological record of AI risk determinations, bounded actions, and human overrides.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setOverrideFilter(!overrideFilter)}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-all flex items-center space-x-1.5 ${
              overrideFilter
                ? 'bg-[#FF8800]/20 text-[#FF8800] border-[#FF8800]/40'
                : 'bg-[#0B1E36] text-slate-300 border-[#1B3558] hover:text-white hover:bg-[#132E52]'
            }`}
          >
            <UserCheck className="w-3.5 h-3.5" />
            <span>Human Overrides Only</span>
          </button>

          <button
            onClick={fetchLogs}
            className="p-2 bg-[#0B1E36] border border-[#1B3558] rounded-lg text-slate-300 hover:text-white"
            title="Refresh logs"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="bg-[#0B1E36] border border-[#1B3558] rounded-xl overflow-hidden shadow-sm">
        {loading ? (
          <div className="p-12 text-center text-slate-400 text-xs flex items-center justify-center space-x-2">
            <RefreshCw className="w-4 h-4 animate-spin text-[#0066FF]" />
            <span className="font-semibold">Loading audit trail...</span>
          </div>
        ) : logs.length === 0 ? (
          <div className="p-12 text-center text-slate-400 text-xs">
            No audit records found matching criteria.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-[#07162A] border-b border-[#1B3558] text-slate-400 uppercase tracking-wider font-extrabold text-[10px]">
                <tr>
                  <th className="py-3 px-4 font-sans">Timestamp (UTC)</th>
                  <th className="py-3 px-4">Transaction Reference</th>
                  <th className="py-3 px-4">Score</th>
                  <th className="py-3 px-4 font-sans">Risk Level</th>
                  <th className="py-3 px-4">AI Rec</th>
                  <th className="py-3 px-4">Final Action</th>
                  <th className="py-3 px-4 font-sans">Decision Mode</th>
                  <th className="py-3 px-4 font-sans">Operator & Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1B3558]/60 font-medium">
                {logs.map((log) => (
                  <tr key={log.id} className="hover:bg-[#07162A]/50 transition-all">
                    <td className="py-3 px-4 text-slate-400 text-[11px] font-sans">
                      {log.timestamp ? new Date(log.timestamp).toLocaleTimeString() : 'N/A'}
                    </td>
                    <td className="py-3 px-4 font-extrabold text-white">
                      {log.transaction_id}
                    </td>
                    <td className="py-3 px-4">
                      <span className={`${
                        log.risk_score >= 70 ? 'text-[#FF334B]' :
                        log.risk_score >= 30 ? 'text-[#FF8800]' : 'text-[#00B368]'
                      } font-extrabold`}>
                        {log.risk_score}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-sans">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        log.risk_level === 'HIGH' ? 'bg-[#FF334B]/15 text-[#FF334B] border border-[#FF334B]/30' :
                        log.risk_level === 'MEDIUM' ? 'bg-[#FF8800]/15 text-[#FF8800] border border-[#FF8800]/30' :
                        'bg-[#00B368]/15 text-[#00B368] border border-[#00B368]/30'
                      }`}>
                        {log.risk_level}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-400">{log.recommended_action}</td>
                    <td className="py-3 px-4 font-bold text-white">{log.final_action}</td>
                    <td className="py-3 px-4 font-sans">
                      {log.human_override ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-[#FF8800]/20 text-[#FF8800] border border-[#FF8800]/40">
                          <UserCheck className="w-3 h-3 mr-1" />
                          Human Override
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-[#0066FF]/15 text-[#3395FF] border border-[#0066FF]/30">
                          AI Autonomous
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4 font-sans text-slate-300 text-[11px] max-w-xs truncate" title={log.decision_reason}>
                      <span className="font-bold text-white">{log.operator_name}: </span>
                      {log.decision_reason || 'Autonomous risk decision'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
