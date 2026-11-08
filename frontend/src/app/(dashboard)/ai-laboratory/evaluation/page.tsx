export default function AIEvaluationPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Model Evaluation & Benchmarking</h1>
        <p className="text-sm text-slate-500 mt-1">Validation metrics including MAE, RMSE, WAPE, and ROC-AUC curves.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Aggregate MAE</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">42.1 Units</div>
          <div className="text-xs text-emerald-600 mt-1">-8.4% error reduction</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Root Mean Squared Error</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">58.7</div>
          <div className="text-xs text-slate-500 mt-1">Evaluated across 1,820 SKUs</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Stockout ROC-AUC</div>
          <div className="text-2xl font-bold text-blue-600 mt-2">0.962</div>
          <div className="text-xs text-blue-700 mt-1">High sensitivity classification</div>
        </div>
      </div>
    </div>
  );
}
