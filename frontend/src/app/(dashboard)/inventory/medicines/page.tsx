export default function MedicinesCatalogPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Medicines Catalog</h1>
        <p className="text-sm text-slate-500 mt-1">Directory of registered pharmaceutical drugs, dosages, formulations, and active ingredients.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Registered Medicines</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">1,820</div>
          <div className="text-xs text-emerald-600 mt-1">Compliant with WHO Essential Medicines</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Therapeutic Categories</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">48</div>
          <div className="text-xs text-blue-600 mt-1">Antibiotics, Cardiovascular, Oncology, etc.</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Cold Chain Items</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">320</div>
          <div className="text-xs text-amber-600 mt-1">Temperature sensitive (2°C - 8°C)</div>
        </div>
      </div>
    </div>
  );
}
