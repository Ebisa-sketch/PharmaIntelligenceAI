export default function DashboardOverviewPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Executive Dashboard</h1>
        <p className="text-sm text-slate-500 mt-1">Comprehensive overview of supply chain health, risk indicators, and inventory metrics.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Medicines Tracked</div>
          <div className="text-3xl font-bold text-slate-900 mt-2">14,820</div>
          <div className="text-xs text-emerald-600 mt-1">+124 added this month</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Stockout Risk Alerts</div>
          <div className="text-3xl font-bold text-amber-600 mt-2">18</div>
          <div className="text-xs text-amber-700 mt-1">Requires immediate review</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Expiring in 60 Days</div>
          <div className="text-3xl font-bold text-rose-600 mt-2">34 Batches</div>
          <div className="text-xs text-rose-700 mt-1">Redistribution recommended</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Forecast Model Accuracy</div>
          <div className="text-3xl font-bold text-blue-600 mt-2">94.8%</div>
          <div className="text-xs text-blue-700 mt-1">WAPE: 5.2% across regions</div>
        </div>
      </div>

      <div className="p-6 bg-white rounded-xl border border-slate-200 shadow-sm space-y-4">
        <h2 className="text-base font-semibold text-slate-900">Supply Chain Operations Summary</h2>
        <p className="text-sm text-slate-600 leading-relaxed">
          Welcome to PharmaIntelligence AI. The system has completed morning automated inference across regional hospital networks and distribution hubs.
        </p>
      </div>
    </div>
  );
}
