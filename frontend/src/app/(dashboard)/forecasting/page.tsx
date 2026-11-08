'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { forecastingApi, facilitiesApi, medicinesApi } from '@/lib/api';
import { ForecastResponse, Facility, Medicine } from '@/types';
import {
  TrendingUp,
  Sliders,
  Calendar,
  Sparkles,
  Info,
  Layers,
  ArrowRight,
  ShieldCheck,
} from 'lucide-react';
import Link from 'next/link';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

export default function DemandForecastingPage() {
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<number>(1);
  const [selectedMedicine, setSelectedMedicine] = useState<number>(1);
  const [horizonDays, setHorizonDays] = useState<number>(90);
  const [modelType, setModelType] = useState<string>('ensemble');
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadInitial() {
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
    loadInitial();
  }, []);

  useEffect(() => {
    async function loadForecast() {
      setIsLoading(true);
      try {
        const data = await forecastingApi.getForecast(
          selectedFacility,
          selectedMedicine,
          horizonDays,
          modelType
        );
        setForecast(data);
      } catch (err) {
        console.error('Failed to load forecast:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadForecast();
  }, [selectedFacility, selectedMedicine, horizonDays, modelType]);

  const currentMed = medicines.find((m) => m.id === selectedMedicine);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Demand Forecasting Hub
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Intermittent demand forecasting with Syntetos-Boylan classification, Croston-SBA, and HistGradientBoosting.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link href="/forecasting/model-comparison">
            <Button variant="outline" size="sm">
              <Layers className="w-3.5 h-3.5 mr-1.5" />
              Algorithm Benchmark &amp; Comparison
            </Button>
          </Link>
        </div>
      </div>

      {/* Control Selector Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
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
                {m.name} ({m.dosage_form})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-1">
            Prediction Horizon
          </label>
          <select
            value={horizonDays}
            onChange={(e) => setHorizonDays(Number(e.target.value))}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value={30}>30 Days (Short-term)</option>
            <option value={60}>60 Days (Mid-term)</option>
            <option value={90}>90 Days (Quarterly Plan)</option>
          </select>
        </div>

        <div>
          <label className="block text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-1">
            Forecasting Model
          </label>
          <select
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="ensemble">Ensemble (HistGB + Croston + Holt-Winters)</option>
            <option value="gradient_boosting">HistGradientBoosting (XGB)</option>
            <option value="croston_sba">Croston-SBA (Intermittent)</option>
            <option value="exponential_smoothing">Holt-Winters Exponential Smoothing</option>
          </select>
        </div>
      </div>

      {/* Forecast Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Total Projected Demand
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-1">
            {forecast?.summary.total_projected_demand.toLocaleString()} units
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">
            Over {horizonDays} days horizon
          </div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Average Daily Demand
          </div>
          <div className="text-2xl font-bold text-blue-600 mt-1">
            {forecast?.summary.daily_average_demand.toFixed(1)} units/day
          </div>
          <div className="text-[11px] text-blue-700 mt-0.5">
            De-censored for stockout gaps
          </div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Recommended Safety Buffer
          </div>
          <div className="text-2xl font-bold text-emerald-600 mt-1">
            {forecast?.summary.recommended_safety_stock.toLocaleString()} units
          </div>
          <div className="text-[11px] text-emerald-700 mt-0.5">
            95% service level protection
          </div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Demand Pattern
          </div>
          <div className="text-sm font-bold text-slate-800 mt-1 truncate">
            {forecast?.summary.demand_pattern || 'Steady'}
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">
            {forecast?.summary.volatility}
          </div>
        </div>
      </div>

      {/* Recharts Forecast Graph with P10 - P90 Bands */}
      <Card
        title={`Probabilistic Demand Trajectory: ${currentMed?.name || 'Selected Medicine'}`}
        subtitle={`Historical consumption and projected P10 (optimistic), P50 (expected), and P90 (surge) trajectories`}
      >
        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={forecast?.points || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="date" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  color: '#fff',
                  borderRadius: '8px',
                  fontSize: '12px',
                }}
              />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              <Area
                type="monotone"
                dataKey="p90"
                name="Surge Threshold (P90)"
                stroke="#93c5fd"
                fill="#dbeafe"
                fillOpacity={0.4}
              />
              <Area
                type="monotone"
                dataKey="p50"
                name="Projected Demand (P50)"
                stroke="#2563eb"
                strokeWidth={2.5}
                fill="none"
              />
              <Area
                type="monotone"
                dataKey="p10"
                name="Base Demand (P10)"
                stroke="#bfdbfe"
                fill="none"
              />
              <Area
                type="monotone"
                dataKey="historical_consumption"
                name="Historical Dispensing"
                stroke="#059669"
                strokeWidth={2}
                fill="none"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* XAI Explainability Card */}
      <div className="bg-slate-900 rounded-xl text-slate-100 p-6 space-y-3">
        <div className="flex items-center gap-2 text-blue-400 text-xs font-semibold uppercase tracking-wider">
          <Sparkles className="w-4 h-4" />
          Explainable AI (XAI) Model Diagnostics
        </div>
        <div className="text-sm text-slate-300 leading-relaxed">
          The forecast incorporates <strong className="text-white">Syntetos-Boylan ADI / CV² classification</strong>, stockout de-censoring
          to correct for zero-dispensing days during stock depletion, and seasonality adjustments aligned with regional Ethiopian disease
          transmission patterns. P90 surge buffer protects clinical continuity during supply delays.
        </div>
      </div>
    </div>
  );
}
