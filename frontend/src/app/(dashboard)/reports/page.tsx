export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Analytical Reports</h1>
        <p className="text-sm text-slate-500 mt-1">Customizable PDF/CSV reports on inventory velocity, supply chain resiliency, and costs.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Scheduled Exports</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">12 Active</div>
          <div className="text-xs text-slate-500 mt-1">Sent to regional directors</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Financial Savings Report</div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">Ready</div>
          <div className="text-xs text-emerald-700 mt-1">Q3 Wastage Prevention Analysis</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Compliance Audit Report</div>
          <div className="text-2xl font-bold text-blue-600 mt-2">Generated</div>
          <div className="text-xs text-blue-700 mt-1">GMP & Traceability standard</div>
        </div>
      </div>
    </div>
  );
}
