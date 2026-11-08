export default function AIExperimentsPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Experiment Tracker</h1>
        <p className="text-sm text-slate-500 mt-1">Catalog of ML training runs, datasets, feature engineering iterations, and loss curves.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Runs Logged</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">142</div>
          <div className="text-xs text-slate-500 mt-1">Tracked via MLflow / Weights & Biases</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Best Validation WAPE</div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">3.82%</div>
          <div className="text-xs text-emerald-700 mt-1">Run #139: Multi-layer Perceptron Ensemble</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Compute Utilization</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">68%</div>
          <div className="text-xs text-blue-600 mt-1">4x NVIDIA A10G Instances</div>
        </div>
      </div>
    </div>
  );
}
