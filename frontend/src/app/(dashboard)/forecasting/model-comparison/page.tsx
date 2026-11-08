'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { forecastingApi, facilitiesApi, medicinesApi } from '@/lib/api';
import { ModelComparisonResponse, Facility, Medicine } from '@/types';
import { Layers, ArrowLeft, Trophy, CheckCircle2, BarChart2 } from 'lucide-react';
import Link from 'next/link';

export default function ModelComparisonPage() {
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<number>(1);
  const [selectedMedicine, setSelectedMedicine] = useState<number>(1);
  const [comparison, setComparison] = useState<ModelComparisonResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadMeta() {
      try {
        const [facs, meds] = await Promise.all([
          facilitiesApi.list(),
          medicinesApi.list(),
        ]);
        setFacilities(facs);
        setMedicines(meds);
      } catch (err) {
        console.error('Failed to load metadata:', err);
      }
    }
    loadMeta();
  }, []);

  useEffect(() => {
    async function loadComparison() {
      setIsLoading(true);
      try {
        const res = await forecastingApi.compareModels(selectedFacility, selectedMedicine);
        setComparison(res);
      } catch (err) {
        console.error('Failed to load model comparison:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadComparison();
  }, [selectedFacility, selectedMedicine]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200/80 pb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Link
              href="/forecasting"
              className="text-xs text-blue-600 hover:text-blue-700 font-medium flex items-center"
            >
              <ArrowLeft className="w-3.5 h-3.5 mr-1" /> Back to Forecasting
            </Link>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Forecasting Algorithm Benchmark &amp; Comparison
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Empirical evaluation of candidate algorithms using Syntetos-Boylan demand categorization and error metrics.
          </p>
        </div>
      </div>

      {/* Selectors */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
        <div>
          <label className="block text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-1">
            Facility
          </label>
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
          <label className="block text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-1">
            Medicine
          </label>
          <select
            value={selectedMedicine}
            onChange={(e) => setSelectedMedicine(Number(e.target.value))}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            {medicines.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Syntetos-Boylan Classification Card */}
      {comparison && (
        <div className="p-5 bg-blue-900 text-white rounded-xl shadow-md flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-1.5">
            <div className="text-xs font-semibold uppercase text-blue-300 tracking-wider">
              Syntetos-Boylan Demand Classification
            </div>
            <h2 className="text-2xl font-bold">
              {comparison.syntetos_boylan_class} Demand Series
            </h2>
            <p className="text-xs text-blue-200 max-w-xl">
              {comparison.classification_rationale}
            </p>
          </div>
          <div className="flex items-center gap-4 shrink-0">
            <div className="text-center p-3 rounded-lg bg-white/10">
              <div className="text-[10px] text-blue-200 uppercase font-semibold">ADI (Inter-arrival)</div>
              <div className="text-lg font-bold text-white mt-0.5">{(comparison.adi ?? 0).toFixed(2)}</div>
            </div>
            <div className="text-center p-3 rounded-lg bg-white/10">
              <div className="text-[10px] text-blue-200 uppercase font-semibold">CV² (Variance)</div>
              <div className="text-lg font-bold text-white mt-0.5">{(comparison.cv2 ?? 0).toFixed(2)}</div>
            </div>
          </div>
        </div>
      )}

      {/* Comparison Metrics Table */}
      <Card
        title="Candidate Models Error Matrix"
        subtitle="Ranked by Weighted Absolute Percentage Error (WAPE) and Mean Absolute Scaled Error (MASE)"
      >
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
              <tr>
                <th className="px-6 py-3.5">Rank</th>
                <th className="px-6 py-3.5">Algorithm Name</th>
                <th className="px-6 py-3.5">WAPE (%)</th>
                <th className="px-6 py-3.5">RMSE</th>
                <th className="px-6 py-3.5">MAE</th>
                <th className="px-6 py-3.5">MASE</th>
                <th className="px-6 py-3.5 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {comparison?.models.map((m) => (
                <tr key={m.model_name} className={m.recommended ? 'bg-blue-50/40 font-semibold' : 'hover:bg-slate-50/60'}>
                  <td className="px-6 py-3.5">
                    {m.recommended ? (
                      <span className="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xs">
                        1
                      </span>
                    ) : (
                      <span className="text-slate-400 font-bold ml-2">{m.rank}</span>
                    )}
                  </td>
                  <td className="px-6 py-3.5 font-medium text-slate-900 flex items-center gap-2">
                    {m.model_name}
                    {m.recommended && (
                      <Badge variant="info" size="sm">
                        Recommended
                      </Badge>
                    )}
                  </td>
                  <td className="px-6 py-3.5 text-blue-700 font-bold">
                    {(m.wape ?? 0).toFixed(1)}%
                  </td>
                  <td className="px-6 py-3.5 text-slate-600">{(m.rmse ?? 0).toFixed(2)}</td>
                  <td className="px-6 py-3.5 text-slate-600">{(m.mae ?? 0).toFixed(2)}</td>
                  <td className="px-6 py-3.5 text-slate-600">{(m.mase ?? 0).toFixed(2)}</td>
                  <td className="px-6 py-3.5 text-right">
                    {m.recommended ? (
                      <span className="text-emerald-600 text-xs font-semibold flex items-center justify-end gap-1">
                        <CheckCircle2 className="w-4 h-4" /> Active in Production
                      </span>
                    ) : (
                      <span className="text-slate-400 text-xs">Alternative</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
