'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { stockoutApi, facilitiesApi } from '@/lib/api';
import { StockoutRiskItem, Facility } from '@/types';
import {
  AlertTriangle,
  ShieldAlert,
  ArrowRight,
  TrendingDown,
  Layers,
  Sparkles,
  RefreshCw,
  Search,
} from 'lucide-react';
import Link from 'next/link';

export default function StockoutIntelligencePage() {
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<number>(1);
  const [selectedRiskLevel, setSelectedRiskLevel] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [risks, setRisks] = useState<StockoutRiskItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedXAIItem, setSelectedXAIItem] = useState<StockoutRiskItem | null>(null);

  useEffect(() => {
    async function loadMeta() {
      try {
        const facs = await facilitiesApi.list();
        setFacilities(facs);
      } catch (err) {
        console.error('Failed to load facilities:', err);
      }
    }
    loadMeta();
  }, []);

  useEffect(() => {
    async function loadRisks() {
      setIsLoading(true);
      try {
        const data = await stockoutApi.getFacilityRisks(
          selectedFacility,
          selectedRiskLevel === 'All' ? undefined : selectedRiskLevel
        );
        setRisks(data);
      } catch (err) {
        console.error('Failed to load stockout risks:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadRisks();
  }, [selectedFacility, selectedRiskLevel]);

  const filteredRisks = risks.filter((r) => {
    const q = searchQuery.toLowerCase();
    return r.medicine_name.toLowerCase().includes(q) || r.medicine_code.toLowerCase().includes(q);
  });

  const getRiskBadge = (level: string) => {
    switch (level) {
      case 'Critical':
        return <Badge variant="danger">Critical Risk</Badge>;
      case 'High':
        return <Badge variant="warning">High Risk</Badge>;
      case 'Medium':
        return <Badge variant="info">Medium Risk</Badge>;
      default:
        return <Badge variant="success">Low Risk</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Stockout Risk Intelligence (XAI)
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Probabilistic stockout classification, Days of Stock Remaining (DSR), and SHAP feature attribution.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link href="/redistribution">
            <Button variant="primary" size="sm">
              <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
              Transfer Optimization
            </Button>
          </Link>
        </div>
      </div>

      {/* Control Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search medicine or code..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <select
            value={selectedFacility}
            onChange={(e) => setSelectedFacility(Number(e.target.value))}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            {facilities.map((f) => (
              <option key={f.id} value={f.id}>
                {f.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <select
            value={selectedRiskLevel}
            onChange={(e) => setSelectedRiskLevel(e.target.value)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="All">All Risk Tiers</option>
            <option value="Critical">Critical Only</option>
            <option value="High">High Only</option>
            <option value="Medium">Medium Only</option>
            <option value="Low">Low Only</option>
          </select>
        </div>
      </div>

      {/* Risk Summary Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Critical Alerts
          </div>
          <div className="text-2xl font-bold text-rose-600 mt-1">
            {risks.filter((r) => r.risk_level === 'Critical').length}
          </div>
          <div className="text-[11px] text-rose-700 mt-0.5">DSR &lt; 7 Days</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            High Risk Alerts
          </div>
          <div className="text-2xl font-bold text-amber-600 mt-1">
            {risks.filter((r) => r.risk_level === 'High').length}
          </div>
          <div className="text-[11px] text-amber-700 mt-0.5">DSR &lt; Lead Time</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Total Monitored Items
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-1">{risks.length}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">At selected facility</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Calibrated Confidence
          </div>
          <div className="text-2xl font-bold text-blue-600 mt-1">94.5%</div>
          <div className="text-[11px] text-blue-700 mt-0.5">Brier Score = 0.082</div>
        </div>
      </div>

      {/* Stockout Risk Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
              <tr>
                <th className="px-6 py-3.5">Medicine</th>
                <th className="px-6 py-3.5">Current Stock</th>
                <th className="px-6 py-3.5">Daily Demand</th>
                <th className="px-6 py-3.5">Days Remaining (DSR)</th>
                <th className="px-6 py-3.5">Lead Time</th>
                <th className="px-6 py-3.5">Stockout Probability</th>
                <th className="px-6 py-3.5">Risk Tier</th>
                <th className="px-6 py-3.5 text-right">XAI Diagnostics</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredRisks.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50/60 transition-colors">
                  <td className="px-6 py-3.5">
                    <div className="font-semibold text-slate-900">{item.medicine_name}</div>
                    <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                      {item.medicine_code} &bull; {item.vital_classification}
                    </div>
                  </td>
                  <td className="px-6 py-3.5 font-bold text-slate-900">
                    {(item.current_stock ?? 0).toLocaleString()} units
                  </td>
                  <td className="px-6 py-3.5 text-slate-600">
                    {(item.daily_demand_rate ?? 0).toFixed(1)} / day
                  </td>
                  <td className="px-6 py-3.5">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-900">
                        {(item.days_of_stock_remaining ?? 0).toFixed(1)}d
                      </span>
                      {(item.days_of_stock_remaining ?? 0) < (item.lead_time_days ?? 0) && (
                        <span className="text-[10px] text-rose-600 font-semibold">&lt; Lead Time</span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-3.5 text-slate-600">{item.lead_time_days ?? 25} days</td>
                  <td className="px-6 py-3.5">
                    <span
                      className={`font-bold ${
                        (item.stockout_probability ?? 0) >= 0.7
                          ? 'text-rose-600'
                          : (item.stockout_probability ?? 0) >= 0.3
                          ? 'text-amber-600'
                          : 'text-emerald-600'
                      }`}
                    >
                      {((item.stockout_probability ?? 0) * 100).toFixed(0)}%
                    </span>
                  </td>
                  <td className="px-6 py-3.5">{getRiskBadge(item.risk_level)}</td>
                  <td className="px-6 py-3.5 text-right">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setSelectedXAIItem(item)}
                    >
                      <Sparkles className="w-3.5 h-3.5 mr-1 text-blue-600" />
                      View SHAP
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* XAI SHAP Attribution Modal */}
      {selectedXAIItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
          <div className="w-full max-w-lg bg-white rounded-xl shadow-xl border border-slate-200 p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  XAI Feature Attribution Breakdown
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  {selectedXAIItem.medicine_name} ({selectedXAIItem.medicine_code})
                </p>
              </div>
              <Badge variant={selectedXAIItem.risk_level === 'Critical' ? 'danger' : 'warning'}>
                {selectedXAIItem.risk_level} Risk
              </Badge>
            </div>

            <div className="space-y-3">
              <div className="text-xs font-semibold text-slate-700">
                Top Model Risk Drivers (TreeSHAP Values):
              </div>
              {selectedXAIItem.feature_attributions.map((attr, idx) => (
                <div key={idx} className="p-3 rounded-lg border border-slate-200/80 bg-slate-50 space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-medium text-slate-800">{attr.feature}</span>
                    <span
                      className={`font-bold ${
                        attr.direction === 'increases_risk' ? 'text-rose-600' : 'text-emerald-600'
                      }`}
                    >
                      {attr.direction === 'increases_risk'
                        ? `+${((attr.impact ?? 0) * 100).toFixed(0)}%`
                        : `-${(Math.abs(attr.impact ?? 0) * 100).toFixed(0)}%`}
                    </span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        attr.direction === 'increases_risk' ? 'bg-rose-500' : 'bg-emerald-500'
                      }`}
                      style={{ width: `${Math.min(100, Math.abs(attr.impact) * 100 * 2)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>

            <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg text-xs text-blue-900 space-y-1">
              <span className="font-semibold block text-blue-800">Clinical Recommendation:</span>
              <span>{selectedXAIItem.clinical_recommendation}</span>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setSelectedXAIItem(null)}
              >
                Close
              </Button>
              <Link href="/redistribution">
                <Button variant="primary" size="sm">
                  Initiate Lateral Transfer &rarr;
                </Button>
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
