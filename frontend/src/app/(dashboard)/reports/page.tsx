'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { reportsApi, facilitiesApi } from '@/lib/api';
import { SystemSummary, Facility } from '@/types';
import {
  FileBarChart2,
  Download,
  Building2,
  Calendar,
  FileCheck,
  TrendingUp,
  AlertTriangle,
  Clock,
} from 'lucide-react';

export default function ReportsPage() {
  const [summary, setSummary] = useState<SystemSummary | null>(null);
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [sum, facs] = await Promise.all([
          reportsApi.getSummary(),
          facilitiesApi.list(),
        ]);
        setSummary(sum);
        setFacilities(facs);
      } catch (err) {
        console.error('Failed to load reports summary:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  const reportsList = [
    {
      title: 'National Stockout Risk & Lead-Time Gap Audit',
      date: 'Current Month',
      type: 'Risk Surveillance',
      summary: 'Probabilistic DSR analysis across 8 regional hubs with lead time deficit evaluation.',
    },
    {
      title: 'FEFO Expiry Prevention & Lateral Transfer Feasibility',
      date: 'Bi-Weekly',
      type: 'Optimization',
      summary: 'Evaluation of 34 near-expiry batches and net financial savings in Ethiopian Birr (ETB).',
    },
    {
      title: 'Data Quality Index (DQI) & Cleansing Summary',
      date: 'Weekly',
      type: 'Governance',
      summary: '5D DQI scores assessing Completeness, Consistency, Plausibility, Validity, and Uniqueness.',
    },
    {
      title: 'Intermittent Demand Forecasting Model Accuracy (WAPE/MASE)',
      date: 'Monthly',
      type: 'AI Diagnostics',
      summary: 'Benchmarking Croston-SBA vs HistGradientBoosting across Syntetos-Boylan demand types.',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Supply Chain Reports &amp; Analytics
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Executive audit summaries, regulatory compliance packages, and mathematical optimization metrics.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={() => alert('Exporting comprehensive report PDF...')}>
            <Download className="w-3.5 h-3.5 mr-1.5" />
            Export Executive PDF
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-5 bg-white rounded-xl border border-slate-200/80 shadow-xs space-y-1">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Total Monitored Items
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {summary?.total_inventory_items || 80} SKU Records
          </div>
          <div className="text-xs text-slate-500">Across {facilities.length} teaching hospitals</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200/80 shadow-xs space-y-1">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Critical Stockout Alert Count
          </div>
          <div className="text-2xl font-bold text-rose-600">
            {summary?.critical_stockouts || 7}
          </div>
          <div className="text-xs text-rose-700">Stock runout requiring immediate intervention</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200/80 shadow-xs space-y-1">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            DQI Data Quality Score
          </div>
          <div className="text-2xl font-bold text-emerald-600">
            {summary?.average_dqi_score || 93.6}%
          </div>
          <div className="text-xs text-emerald-700">Grade A (Optimal for AI inference)</div>
        </div>
      </div>

      {/* Standard Reports List */}
      <div className="space-y-3">
        <h3 className="text-sm font-semibold text-slate-900">Available Governance &amp; Operational Reports</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {reportsList.map((r, idx) => (
            <div
              key={idx}
              className="p-5 bg-white rounded-xl border border-slate-200/80 shadow-xs flex flex-col justify-between space-y-3 hover:border-blue-300 transition-colors"
            >
              <div>
                <div className="flex items-center justify-between gap-2">
                  <Badge variant="info">{r.type}</Badge>
                  <span className="text-[11px] text-slate-400 font-medium">{r.date}</span>
                </div>
                <h4 className="font-bold text-slate-900 text-sm mt-2">{r.title}</h4>
                <p className="text-xs text-slate-500 mt-1">{r.summary}</p>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                <span className="text-[11px] text-slate-400">PDF &bull; CSV &bull; Excel</span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => alert(`Generating download for: ${r.title}`)}
                >
                  <Download className="w-3.5 h-3.5 mr-1" />
                  Download
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
