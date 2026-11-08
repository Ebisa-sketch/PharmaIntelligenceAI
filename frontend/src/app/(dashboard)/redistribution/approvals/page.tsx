export default function RedistributionApprovalsPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Transfer Approvals & Dispatch</h1>
        <p className="text-sm text-slate-500 mt-1">Workflow management for pharmacists and logistics managers to review and execute transfers.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Pending Pharmacist Sign-Off</div>
          <div className="text-2xl font-bold text-amber-600 mt-2">3</div>
          <div className="text-xs text-amber-700 mt-1">Awaiting clinical approval</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Pending Logistics Dispatch</div>
          <div className="text-2xl font-bold text-blue-600 mt-2">5</div>
          <div className="text-xs text-blue-700 mt-1">Driver assigned, in transit</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Average Approval Time</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">26 mins</div>
          <div className="text-xs text-emerald-600 mt-1">Fast-track workflow enabled</div>
        </div>
      </div>
    </div>
  );
}
