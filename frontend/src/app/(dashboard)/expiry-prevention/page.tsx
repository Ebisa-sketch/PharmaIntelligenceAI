export default function ExpiryPreventionPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Expiry Prevention Center</h1>
        <p className="text-sm text-slate-500 mt-1">Minimizing drug wastage through proactive expiry tracking and FEFO policy automation.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Near-Expiry Value at Risk</div>
          <div className="text-2xl font-bold text-amber-600 mt-2">$24,180</div>
          <div className="text-xs text-slate-500 mt-1">Batches expiring within 90 days</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Wastage Saved YTD</div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">$182,500</div>
          <div className="text-xs text-emerald-700 mt-1">Through automated redistribution</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Expiry Rate</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">0.42%</div>
          <div className="text-xs text-emerald-600 mt-1">Well below industry benchmark (1.8%)</div>
        </div>
      </div>
    </div>
  );
}
