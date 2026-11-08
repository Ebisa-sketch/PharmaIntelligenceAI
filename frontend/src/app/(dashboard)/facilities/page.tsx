export default function FacilitiesPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Healthcare Facilities Directory</h1>
        <p className="text-sm text-slate-500 mt-1">Hospitals, regional clinics, central warehouses, and distribution nodes.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Connected Facilities</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">18</div>
          <div className="text-xs text-emerald-600 mt-1">100% online & syncing</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Central Warehouses</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">3</div>
          <div className="text-xs text-slate-500 mt-1">High-capacity cold storage</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Regional Hospitals</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">15</div>
          <div className="text-xs text-slate-500 mt-1">Serving 2.5M population base</div>
        </div>
      </div>
    </div>
  );
}
