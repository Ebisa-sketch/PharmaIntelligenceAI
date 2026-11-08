export default function DataQualityIssuesPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Data Quality Issues</h1>
        <p className="text-sm text-slate-500 mt-1">Triage and remediation queue for missing records, duplicate SKUs, and anomalous entries.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Critical Issues</div>
          <div className="text-2xl font-bold text-rose-600 mt-2">1</div>
          <div className="text-xs text-rose-700 mt-1">Unit mismatch in Facility #4</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Warning Level</div>
          <div className="text-2xl font-bold text-amber-600 mt-2">4</div>
          <div className="text-xs text-amber-700 mt-1">Minor timestamp drift</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Resolved Today</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">12</div>
          <div className="text-xs text-emerald-600 mt-1">Remediated & verified</div>
        </div>
      </div>
    </div>
  );
}
