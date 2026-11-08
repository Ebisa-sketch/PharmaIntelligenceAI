export default function ForecastingAnalysisPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Forecast Trend Analysis</h1>
        <p className="text-sm text-slate-500 mt-1">Seasonality, epidemic trends, weather correlation, and confidence intervals.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Seasonal Coefficient</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">+18.2%</div>
          <div className="text-xs text-blue-600 mt-1">Winter respiratory peak detected</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Epidemic Risk Signal</div>
          <div className="text-2xl font-bold text-amber-600 mt-2">Moderate</div>
          <div className="text-xs text-amber-700 mt-1">Elevated influenza caseload in North Region</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Confidence Interval</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">95%</div>
          <div className="text-xs text-slate-500 mt-1">P10 - P90 spread within target bound</div>
        </div>
      </div>
    </div>
  );
}
