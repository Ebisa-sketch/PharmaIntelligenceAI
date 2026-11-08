export default function InventoryPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Inventory Overview</h1>
        <p className="text-sm text-slate-500 mt-1">Real-time monitoring of pharmaceutical inventory levels across all healthcare facilities.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Active Inventory SKUs</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">2,415</div>
          <div className="text-xs text-emerald-600 mt-1">✓ Across 12 regional facilities</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Inventory Valuation</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">$4.82M</div>
          <div className="text-xs text-slate-500 mt-1">Current total market value</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Turnover Rate</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">8.4x / year</div>
          <div className="text-xs text-blue-600 mt-1">+0.8x vs last quarter</div>
        </div>
      </div>

      <div className="p-6 bg-white rounded-xl border border-slate-200 shadow-sm">
        <h2 className="text-base font-semibold text-slate-900 mb-2">Central Stock Status</h2>
        <p className="text-sm text-slate-600">Track and manage inventory across all connected storage locations, hospitals, and pharmacies.</p>
      </div>
    </div>
  );
}
