export default function DataQualityReportsPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Data Quality Reports</h1>
        <p className="text-sm text-slate-500 mt-1">Historical audit reports and automated validation summaries across hospital networks.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Reports Generated</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">52</div>
          <div className="text-xs text-slate-500 mt-1">Weekly compliance snapshots</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Audit Pass Rate</div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">99.8%</div>
          <div className="text-xs text-emerald-700 mt-1">Meets regulatory standards</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Next Scheduled Run</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">Tonight 00:00</div>
          <div className="text-xs text-blue-600 mt-1">Automated batch validation</div>
        </div>
      </div>
    </div>
  );
}
