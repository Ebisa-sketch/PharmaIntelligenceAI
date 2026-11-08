export default function ForecastingPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Demand Forecasting Hub</h1>
        <p className="text-sm text-slate-500 mt-1">Predictive analytics on pharmaceutical demand using machine learning ensembles.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Forecast Horizon</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">90 Days</div>
          <div className="text-xs text-slate-500 mt-1">Daily granularity predictions</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Mean Absolute Error</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">3.4%</div>
          <div className="text-xs text-emerald-600 mt-1">Benchmark top tier precision</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Active ML Models</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">4 Ensembles</div>
          <div className="text-xs text-blue-600 mt-1">LightGBM + Prophet + XGBoost + LSTM</div>
        </div>
      </div>
    </div>
  );
}
