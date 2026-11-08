export default function DataQualityPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Data Quality & Validation</h1>
        <p className="text-sm text-slate-500 mt-1">Data health checks, anomaly detection, schema adherence, and reconciliation metrics.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Overall Health Score</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">99.4%</div>
          <div className="text-xs text-emerald-600 mt-1">High fidelity data pipeline</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Open Anomalies</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">5</div>
          <div className="text-xs text-amber-600 mt-1">Pending verification</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Automated Cleansings</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">1,490</div>
          <div className="text-xs text-blue-600 mt-1">Resolved automatically this month</div>
        </div>
      </div>
    </div>
  );
}
