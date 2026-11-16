'use client';

import { useState, useEffect } from 'react';
import { 
  AlertOctagon, 
  ShieldAlert, 
  TrendingDown, 
  Clock, 
  HelpCircle, 
  Activity, 
  RefreshCw,
  Search,
  Filter,
  CheckCircle2
} from 'lucide-react';
import { stockoutApi, facilitiesApi } from '@/lib/api';
import { StockoutRiskItem, Facility } from '@/types';
import DemoAlert from '@/components/ui/DemoAlert';

export default function StockoutRiskDetailsPage() {
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<number>(1);
  const [riskItems, setRiskItems] = useState<StockoutRiskItem[]>([]);
  const [selectedItem, setSelectedItem] = useState<StockoutRiskItem | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadFacilities();
  }, []);

  useEffect(() => {
    if (selectedFacility) {
      loadRisks(selectedFacility);
    }
  }, [selectedFacility]);

  const loadFacilities = async () => {
    try {
      const data = await facilitiesApi.list();
      setFacilities(data);
      if (data.length > 0) setSelectedFacility(data[0].id);
    } catch {
      // Fallback
    }
  };

  const loadRisks = async (facId: number) => {
    setIsLoading(true);
    try {
      const data = await stockoutApi.getFacilityRisks(facId);
      setRiskItems(data);
      if (data.length > 0) setSelectedItem(data[0]);
    } catch {
      // Fallback
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <DemoAlert 
        title="Explainable AI (XAI) Stockout Attribution"
        description="Feature contribution weights derived from SHAP/tree-based models, displaying exact drivers for stockout risk (lead time variability, consumption surges, DSR depletion)."
      />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Explainable Stockout Risk Assessment</h1>
          <p className="text-sm text-slate-500 mt-1">
            Deep-dive feature attribution and predictive lead time analysis for critical pharmaceutical stockouts.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-xs font-semibold text-slate-600">Facility:</label>
          <select
            value={selectedFacility}
            onChange={(e) => setSelectedFacility(Number(e.target.value))}
            className="text-xs border border-slate-300 rounded-lg px-2.5 py-1.5 bg-white text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {facilities.map(f => (
              <option key={f.id} value={f.id}>{f.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Medicine Risk List */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Evaluated Medicines ({riskItems.length})
          </div>

          <div className="space-y-2">
            {riskItems.length === 0 ? (
              <div className="p-8 text-center text-xs text-slate-500">No stockout risks detected for this facility.</div>
            ) : (
              riskItems.map((item) => (
                <div
                  key={item.medicine_id}
                  onClick={() => setSelectedItem(item)}
                  className={`p-3.5 rounded-lg border cursor-pointer transition ${
                    selectedItem?.medicine_id === item.medicine_id
                      ? 'border-blue-500 bg-blue-50/60 shadow-xs'
                      : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-900">{item.medicine_name}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      item.risk_level === 'High' || item.risk_level === 'Critical'
                        ? 'bg-rose-100 text-rose-800'
                        : item.risk_level === 'Medium'
                        ? 'bg-amber-100 text-amber-800'
                        : 'bg-emerald-100 text-emerald-800'
                    }`}>
                      {item.risk_level}
                    </span>
                  </div>

                  <div className="text-[11px] text-slate-500 mt-1 flex items-center justify-between">
                    <span>Stock: {item.current_stock.toLocaleString()} units</span>
                    <span>DSR: {item.days_of_stock_remaining.toFixed(1)} days</span>
                  </div>

                  <div className="mt-2 w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                    <div 
                      className={`h-full ${item.stockout_probability > 0.6 ? 'bg-rose-600' : item.stockout_probability > 0.3 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                      style={{ width: `${Math.min(100, item.stockout_probability * 100)}%` }}
                    />
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Selected Item Deep-Dive */}
        <div className="lg:col-span-2 space-y-6">
          {selectedItem ? (
            <>
              {/* Top Summary Card */}
              <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                  <div>
                    <span className="text-xs font-mono text-slate-400">{selectedItem.medicine_code}</span>
                    <h3 className="text-lg font-bold text-slate-900 mt-0.5">{selectedItem.medicine_name}</h3>
                    <div className="text-xs text-slate-500">{selectedItem.facility_name}</div>
                  </div>

                  <div className="text-right">
                    <div className="text-xs text-slate-500">Stockout Probability</div>
                    <div className="text-2xl font-bold text-rose-600">
                      {(selectedItem.stockout_probability * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <div className="text-[10px] text-slate-500 uppercase font-semibold">Current Stock</div>
                    <div className="text-base font-bold text-slate-900 mt-1">
                      {selectedItem.current_stock.toLocaleString()} units
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <div className="text-[10px] text-slate-500 uppercase font-semibold">Daily Run Rate</div>
                    <div className="text-base font-bold text-slate-900 mt-1">
                      {selectedItem.daily_demand_rate.toFixed(1)} / day
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <div className="text-[10px] text-slate-500 uppercase font-semibold">Days of Stock (DSR)</div>
                    <div className="text-base font-bold text-rose-600 mt-1">
                      {selectedItem.days_of_stock_remaining.toFixed(1)} days
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <div className="text-[10px] text-slate-500 uppercase font-semibold">Vendor Lead Time</div>
                    <div className="text-base font-bold text-slate-900 mt-1">
                      {selectedItem.lead_time_days} days
                    </div>
                  </div>
                </div>
              </div>

              {/* Explainable AI Attribution (SHAP Waterfall) */}
              <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-sm font-semibold text-slate-900">Explainable Feature Attribution (SHAP)</h4>
                    <p className="text-xs text-slate-500 mt-0.5">Key drivers pushing risk towards stockout or safety</p>
                  </div>
                  <span className="text-[11px] font-semibold text-slate-500 bg-slate-100 px-2.5 py-1 rounded">
                    Confidence: {(selectedItem.confidence_score * 100).toFixed(0)}%
                  </span>
                </div>

                <div className="space-y-3 pt-2">
                  {selectedItem.feature_attributions.map((attr, idx) => {
                    const isIncrease = attr.direction === 'increases_risk';
                    return (
                      <div key={idx} className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex items-center justify-between gap-4">
                        <div className="space-y-0.5">
                          <div className="text-xs font-semibold text-slate-800">{attr.feature}</div>
                          <div className="text-[10px] text-slate-500">
                            {isIncrease ? 'Accelerates stockout likelihood' : 'Stabilizes inventory buffer'}
                          </div>
                        </div>

                        <div className="text-right shrink-0">
                          <span className={`inline-block px-2 py-0.5 rounded text-xs font-mono font-bold ${
                            isIncrease ? 'bg-rose-100 text-rose-800' : 'bg-emerald-100 text-emerald-800'
                          }`}>
                            {isIncrease ? '+' : ''}{(attr.impact * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Clinical Decision Recommendation */}
              <div className="p-5 bg-blue-50/60 rounded-xl border border-blue-200 space-y-2">
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-blue-700" />
                  <h4 className="text-xs font-bold uppercase tracking-wider text-blue-900">Recommended Clinical Action</h4>
                </div>
                <p className="text-xs text-blue-800 leading-relaxed">
                  {selectedItem.clinical_recommendation}
                </p>
              </div>
            </>
          ) : (
            <div className="p-12 text-center bg-white rounded-xl border border-slate-200">
              <AlertOctagon className="w-10 h-10 text-slate-300 mx-auto mb-2" />
              <p className="text-xs text-slate-500">Select a medicine to view detailed feature attributions.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
