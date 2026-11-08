export default function StockoutRiskDetailsPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Stockout Risk Assessment</h1>
        <p className="text-sm text-slate-500 mt-1">Deep-dive facility-level analysis on stockout probability and critical drug availability.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Highest Risk Facility</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">Memorial General</div>
          <div className="text-xs text-rose-600 mt-1">3 essential antibiotics at risk</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Supplier Lead Time</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">8.2 Days Avg</div>
          <div className="text-xs text-amber-600 mt-1">+2.1 days above contractual baseline</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Automated POs Triggered</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">19</div>
          <div className="text-xs text-blue-600 mt-1">Directly pushed to ERP</div>
        </div>
      </div>
    </div>
  );
}
