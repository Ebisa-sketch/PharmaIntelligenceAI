export default function BatchesPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Batch Management</h1>
        <p className="text-sm text-slate-500 mt-1">Batch-level traceability, manufacturing lot tracking, and quarantine status.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Active Lots</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">4,120</div>
          <div className="text-xs text-emerald-600 mt-1">Fully traceable lots in circulation</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Quarantined Batches</div>
          <div className="text-2xl font-bold text-amber-600 mt-2">3</div>
          <div className="text-xs text-amber-600 mt-1">Under quality investigation</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">FEFO Compliance</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">99.1%</div>
          <div className="text-xs text-emerald-600 mt-1">First-Expired, First-Out adherence</div>
        </div>
      </div>
    </div>
  );
}
