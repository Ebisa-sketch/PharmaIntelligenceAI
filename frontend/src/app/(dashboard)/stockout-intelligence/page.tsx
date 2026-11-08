export default function StockoutIntelligencePage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Stockout Intelligence</h1>
        <p className="text-sm text-slate-500 mt-1">Early warning indicators and proactive alerts for impending medicine stockouts.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Imminent Stockouts (&lt;7 Days)</div>
          <div className="text-2xl font-bold text-rose-600 mt-2">4 SKUs</div>
          <div className="text-xs text-rose-700 mt-1">Critical emergency priority</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Elevated Risk (7-21 Days)</div>
          <div className="text-2xl font-bold text-amber-600 mt-2">14 SKUs</div>
          <div className="text-xs text-amber-700 mt-1">Reorder or transfer needed</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Stockout Prevention Rate</div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">97.8%</div>
          <div className="text-xs text-emerald-700 mt-1">+3.2% vs previous quarter</div>
        </div>
      </div>
    </div>
  );
}
