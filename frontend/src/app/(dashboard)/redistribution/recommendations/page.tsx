export default function RedistributionRecommendationsPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Redistribution Recommendations</h1>
        <p className="text-sm text-slate-500 mt-1">AI-generated transfer routes, cost optimizations, and priority rankings.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">High Priority Transfers</div>
          <div className="text-2xl font-bold text-rose-600 mt-2">4</div>
          <div className="text-xs text-rose-700 mt-1">Immediate shortage relief</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Optimized Logistics Cost</div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">-28%</div>
          <div className="text-xs text-emerald-700 mt-1">Compared to emergency rush reorders</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Model Optimization Method</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">Mixed-Integer LP</div>
          <div className="text-xs text-slate-500 mt-1">Linear programming solver active</div>
        </div>
      </div>
    </div>
  );
}
