export default function RedistributionPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Smart Redistribution Network</h1>
        <p className="text-sm text-slate-500 mt-1">Optimal inter-facility transfers to balance surplus stock with regional shortages.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Active Suggestions</div>
          <div className="text-2xl font-bold text-blue-600 mt-2">15 Transfers</div>
          <div className="text-xs text-blue-700 mt-1">Estimated cost savings: $32,400</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Completed Transfers</div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">128</div>
          <div className="text-xs text-emerald-700 mt-1">This quarter</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Average Transit Time</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">4.2 Hours</div>
          <div className="text-xs text-slate-500 mt-1">Regional cold-chain logistics</div>
        </div>
      </div>
    </div>
  );
}
