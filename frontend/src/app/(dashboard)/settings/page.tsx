export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">System Settings</h1>
        <p className="text-sm text-slate-500 mt-1">Configuration for notification thresholds, API integrations, and model retraining schedules.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Auto-Retrain Frequency</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">Weekly</div>
          <div className="text-xs text-blue-600 mt-1">Sundays at 02:00 UTC</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Stockout Alert Threshold</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">14 Days</div>
          <div className="text-xs text-slate-500 mt-1">Days of supply buffer</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">API Connectors</div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">4 Active</div>
          <div className="text-xs text-slate-500 mt-1">SAP, Epic Systems, Cerner, DHIS2</div>
        </div>
      </div>
    </div>
  );
}
