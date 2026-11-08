'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import {
  reportsApi,
  stockoutApi,
  expiryApi,
  redistributionApi,
} from '@/lib/api';
import {
  SystemSummary,
  StockoutRiskItem,
  ExpiryRiskItem,
  RedistributionProposal,
} from '@/types';
import {
  AlertTriangle,
  Clock,
  Package,
  RefreshCw,
  Building2,
  CheckCircle2,
  ArrowUpRight,
  TrendingUp,
  ShieldAlert,
  ShieldCheck,
  ChevronRight,
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from 'recharts';

// Consumption vs Forecast national trend data
const trendData = [
  { month: 'Jun', actual: 4200, forecast: 4100, lowerBound: 3800, upperBound: 4400 },
  { month: 'Jul', actual: 4450, forecast: 4300, lowerBound: 4000, upperBound: 4600 },
  { month: 'Aug', actual: 4900, forecast: 4800, lowerBound: 4500, upperBound: 5100 },
  { month: 'Sep', actual: 5150, forecast: 5050, lowerBound: 4700, upperBound: 5400 },
  { month: 'Oct', actual: 4800, forecast: 4950, lowerBound: 4600, upperBound: 5300 },
  { month: 'Nov (Live)', actual: 5300, forecast: 5200, lowerBound: 4900, upperBound: 5500 },
  { month: 'Dec (Proj)', actual: null, forecast: 5600, lowerBound: 5100, upperBound: 6100 },
  { month: 'Jan (Proj)', actual: null, forecast: 5850, lowerBound: 5250, upperBound: 6450 },
  { month: 'Feb (Proj)', actual: null, forecast: 6100, lowerBound: 5400, upperBound: 6800 },
];

const facilityStockData = [
  { name: 'Tikur Anbessa', adequate: 62, understocked: 12, stockout: 6 },
  { name: "St. Paul's", adequate: 68, understocked: 8, stockout: 4 },
  { name: 'Jimma UMC', adequate: 55, understocked: 18, stockout: 7 },
  { name: 'Gondar CSH', adequate: 59, understocked: 14, stockout: 7 },
  { name: 'Hawassa CSH', adequate: 64, understocked: 11, stockout: 5 },
];

export default function DashboardOverviewPage() {
  const [summary, setSummary] = useState<SystemSummary | null>(null);
  const [criticalStockouts, setCriticalStockouts] = useState<StockoutRiskItem[]>([]);
  const [expiringBatches, setExpiringBatches] = useState<ExpiryRiskItem[]>([]);
  const [pendingTransfers, setPendingTransfers] = useState<RedistributionProposal[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadDashboardData() {
      try {
        const [sum, stockouts, expiries, transfers] = await Promise.all([
          reportsApi.getSummary(),
          stockoutApi.getFacilityRisks(1),
          expiryApi.getFacilityRisks(1),
          redistributionApi.listRecommendations(undefined, 'Pending'),
        ]);
        setSummary(sum);
        setCriticalStockouts(stockouts.filter((s) => s.risk_level === 'Critical' || s.risk_level === 'High'));
        setExpiringBatches(expiries.slice(0, 3));
        setPendingTransfers(transfers.slice(0, 3));
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadDashboardData();
  }, []);

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/80 pb-5">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Executive Supply Chain Dashboard
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Real-time AI surveillance across Ethiopian regional hospital networks and distribution hubs.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link href="/redistribution">
            <Button variant="primary" size="sm" className="shadow-xs">
              <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
              Run MILP Optimization
            </Button>
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Monitored Facilities */}
        <div className="p-5 bg-white rounded-xl border border-slate-200/80 shadow-xs flex items-center justify-between">
          <div>
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              Connected Facilities
            </div>
            <div className="text-2xl font-bold text-slate-900 mt-1">
              {summary?.total_facilities || 8}
            </div>
            <div className="text-[11px] text-slate-500 mt-0.5">
              Across Addis Ababa, Oromia, Amhara, Sidama
            </div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
            <Building2 className="w-5 h-5" />
          </div>
        </div>

        {/* Critical Stockouts */}
        <div className="p-5 bg-white rounded-xl border border-slate-200/80 shadow-xs flex items-center justify-between">
          <div>
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              Critical Stockout Alerts
            </div>
            <div className="text-2xl font-bold text-rose-600 mt-1">
              {summary?.critical_stockouts || 7}
            </div>
            <div className="text-[11px] text-rose-600 font-medium mt-0.5">
              Immediate action recommended
            </div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-rose-50 text-rose-600 flex items-center justify-center">
            <AlertTriangle className="w-5 h-5" />
          </div>
        </div>

        {/* Expiring Batches */}
        <div className="p-5 bg-white rounded-xl border border-slate-200/80 shadow-xs flex items-center justify-between">
          <div>
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              Batches Expiring &lt;90d
            </div>
            <div className="text-2xl font-bold text-amber-600 mt-1">
              34 Batches
            </div>
            <div className="text-[11px] text-amber-700 font-medium mt-0.5">
              17,380 ETB risk under FEFO
            </div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center">
            <Clock className="w-5 h-5" />
          </div>
        </div>

        {/* Data Quality DQI */}
        <div className="p-5 bg-white rounded-xl border border-slate-200/80 shadow-xs flex items-center justify-between">
          <div>
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              National DQI Index
            </div>
            <div className="text-2xl font-bold text-emerald-600 mt-1">
              {summary?.average_dqi_score || 93.6}%
            </div>
            <div className="text-[11px] text-emerald-700 font-medium mt-0.5">
              Grade A (Optimal for AI inference)
            </div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <CheckCircle2 className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* Analytics Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* National Demand Forecast with Confidence Band */}
        <Card
          title="National Consumption & 90-Day ML Demand Projection"
          subtitle="HistGradientBoosting + Croston ensemble with P10/P90 prediction intervals"
        >
          <div className="h-72 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" stroke="#64748b" fontSize={11} />
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
                  dataKey="upperBound"
                  name="Upper Band (P90)"
                  stroke="#93c5fd"
                  fill="#dbeafe"
                  fillOpacity={0.4}
                />
                <Area
                  type="monotone"
                  dataKey="forecast"
                  name="Forecast (P50)"
                  stroke="#2563eb"
                  strokeWidth={2}
                  fill="none"
                />
                <Area
                  type="monotone"
                  dataKey="actual"
                  name="Historical Dispensing"
                  stroke="#059669"
                  strokeWidth={2.5}
                  fill="none"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Facility Stock Health Distribution */}
        <Card
          title="Regional Facility Inventory Health Distribution"
          subtitle="Proportion of adequate, understocked, and stockout items"
        >
          <div className="h-72 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={facilityStockData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
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
                <Bar dataKey="adequate" name="Adequate" stackId="a" fill="#10b981" />
                <Bar dataKey="understocked" name="Understocked" stackId="a" fill="#f59e0b" />
                <Bar dataKey="stockout" name="Stockout" stackId="a" fill="#ef4444" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      {/* Critical Action Items Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Stockout Risk Action List */}
        <Card
          title="Imminent Stockout Threats"
          subtitle="Probabilistic stockouts based on lead-time vs DSR"
          action={
            <Link
              href="/stockout-intelligence"
              className="text-xs text-blue-600 hover:text-blue-700 font-medium flex items-center"
            >
              View All <ChevronRight className="w-3.5 h-3.5 ml-0.5" />
            </Link>
          }
        >
          <div className="space-y-3">
            {criticalStockouts.map((item, idx) => (
              <div
                key={idx}
                className="p-3 rounded-lg border border-rose-100 bg-rose-50/40 flex items-start justify-between gap-3"
              >
                <div>
                  <div className="text-xs font-semibold text-slate-900">{item.medicine_name}</div>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    Stock: {item.current_stock} units | DSR: {item.days_of_stock_remaining.toFixed(1)} days
                  </div>
                  <div className="text-[11px] text-rose-700 font-medium mt-1">
                    Risk Probability: {(item.stockout_probability * 100).toFixed(0)}%
                  </div>
                </div>
                <Badge variant={item.risk_level === 'Critical' ? 'danger' : 'warning'}>
                  {item.risk_level}
                </Badge>
              </div>
            ))}
          </div>
        </Card>

        {/* Expiry Prevention Candidates */}
        <Card
          title="FEFO Expiry Warnings"
          subtitle="Batches predicted to expire before full depletion"
          action={
            <Link
              href="/expiry-prevention"
              className="text-xs text-blue-600 hover:text-blue-700 font-medium flex items-center"
            >
              View All <ChevronRight className="w-3.5 h-3.5 ml-0.5" />
            </Link>
          }
        >
          <div className="space-y-3">
            {expiringBatches.map((item, idx) => (
              <div
                key={idx}
                className="p-3 rounded-lg border border-amber-100 bg-amber-50/40 flex items-start justify-between gap-3"
              >
                <div>
                  <div className="text-xs font-semibold text-slate-900">{item.medicine_name}</div>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    Lot: {item.batch_number} | Exp: {item.expiry_date}
                  </div>
                  <div className="text-[11px] text-amber-800 font-medium mt-1">
                    PUSE: {item.projected_unused_stock} units ({item.financial_value_at_risk_etb.toLocaleString()} ETB)
                  </div>
                </div>
                <Badge variant={item.risk_level === 'Critical' ? 'danger' : 'warning'}>
                  {item.days_until_expiry}d Left
                </Badge>
              </div>
            ))}
          </div>
        </Card>

        {/* Pending Lateral Redistribution Recommendations */}
        <Card
          title="Pending Lateral Transfers"
          subtitle="MILP optimized cross-facility transfer proposals"
          action={
            <Link
              href="/redistribution"
              className="text-xs text-blue-600 hover:text-blue-700 font-medium flex items-center"
            >
              View All <ChevronRight className="w-3.5 h-3.5 ml-0.5" />
            </Link>
          }
        >
          <div className="space-y-3">
            {pendingTransfers.map((item, idx) => (
              <div
                key={idx}
                className="p-3 rounded-lg border border-blue-100 bg-blue-50/40 flex items-start justify-between gap-3"
              >
                <div>
                  <div className="text-xs font-semibold text-slate-900">{item.medicine_name}</div>
                  <div className="text-[11px] text-slate-600 mt-0.5">
                    {item.source_facility_name} &rarr; {item.target_facility_name}
                  </div>
                  <div className="text-[11px] text-emerald-700 font-medium mt-1">
                    Qty: {item.recommended_quantity} units | Net Saved: {item.net_value_saved_etb.toLocaleString()} ETB
                  </div>
                </div>
                <Badge variant="info">
                  {item.distance_km} km
                </Badge>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
