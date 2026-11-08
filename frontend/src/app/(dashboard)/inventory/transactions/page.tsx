export default function TransactionsPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Inventory Transactions</h1>
        <p className="text-sm text-slate-500 mt-1">Audit logs of inbound shipments, dispensing events, transfers, and disposals.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Transactions Today</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">1,248</div>
          <div className="text-xs text-emerald-600 mt-1">+14% vs daily average</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Pending Dispatches</div>
          <div className="text-2xl font-bold text-blue-600 mt-2">42</div>
          <div className="text-xs text-blue-600 mt-1">Awaiting transport pickup</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Reconciled Rate</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">100%</div>
          <div className="text-xs text-emerald-600 mt-1">No transaction discrepancy detected</div>
        </div>
      </div>
    </div>
  );
}
