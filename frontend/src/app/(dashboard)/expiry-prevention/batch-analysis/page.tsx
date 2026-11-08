export default function ExpiryBatchAnalysisPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Expiry Batch Analysis</h1>
        <p className="text-sm text-slate-500 mt-1">Risk assessment of near-expiry inventory batches and recommended utilization paths.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Critical Batches (&lt;30 Days)</div>
          <div className="text-2xl font-bold text-rose-600 mt-2">7 Batches</div>
          <div className="text-xs text-rose-700 mt-1">High burn-rate facilities alerted</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Moderate Batches (31-90 Days)</div>
          <div className="text-2xl font-bold text-amber-600 mt-2">27 Batches</div>
          <div className="text-xs text-amber-700 mt-1">Targeted for discount or transfer</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Average Shelf Life</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">14.6 Months</div>
          <div className="text-xs text-slate-500 mt-1">Across active pharmaceutical stock</div>
        </div>
      </div>
    </div>
  );
}
