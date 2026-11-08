export default function ModelComparisonPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Forecasting Model Comparison</h1>
        <p className="text-sm text-slate-500 mt-1">Benchmark Prophet, LightGBM, XGBoost, and LSTM model accuracy and error metrics.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">LightGBM (Champion)</div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">4.1% WAPE</div>
          <div className="text-xs text-slate-500 mt-1">Fastest inference latency (12ms)</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Prophet (Challenger)</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">5.8% WAPE</div>
          <div className="text-xs text-slate-500 mt-1">Strong holiday seasonality capture</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">XGBoost</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">4.6% WAPE</div>
          <div className="text-xs text-slate-500 mt-1">Robust against missing regressors</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">LSTM Deep Learning</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">5.2% WAPE</div>
          <div className="text-xs text-slate-500 mt-1">High capacity for long sequence lags</div>
        </div>
      </div>
    </div>
  );
}
