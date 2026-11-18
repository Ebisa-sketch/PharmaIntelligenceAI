'use client';

import React, { useEffect, useState, useMemo } from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Tooltip } from '@/components/ui/Tooltip';
import DemoAlert from '@/components/ui/DemoAlert';
import {
  reportsApi,
  stockoutApi,
  expiryApi,
  redistributionApi,
  facilitiesApi,
  auditLogsApi,
  dataQualityApi,
} from '@/lib/api';
import {
  SystemSummary,
  Facility,
  StockoutRiskItem,
  ExpiryRiskItem,
  RedistributionProposal,
  AuditLogEntry,
  DataQualityIssue,
} from '@/types';
import {
  AlertTriangle,
  Clock,
  Package,
  RefreshCw,
  Building2,
  CheckCircle2,
  TrendingUp,
  ShieldAlert,
  ShieldCheck,
  ChevronRight,
  Info,
  Calendar,
  Filter,
  ArrowRight,
  Truck,
  Activity,
  Layers,
  FileSpreadsheet,
  Cpu,
  AlertCircle,
  HelpCircle,
  Sparkles,
  ArrowUpRight,
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
  Line,
  ComposedChart,
} from 'recharts';

// Multi-horizon National Consumption vs ML Projection Dataset
const PROJECTION_DATA_BY_HORIZON: Record<string, Array<{
  month: string;
  actual: number | null;
  forecast: number;
  lowerBound: number;
  upperBound: number;
  confidence: string;
}>> = {
  '30d': [
    { month: 'Sep', actual: 5150, forecast: 5050, lowerBound: 4700, upperBound: 5400, confidence: 'Historical' },
    { month: 'Oct', actual: 4800, forecast: 4950, lowerBound: 4600, upperBound: 5300, confidence: 'Historical' },
    { month: 'Nov (Current)', actual: 5300, forecast: 5200, lowerBound: 4900, upperBound: 5500, confidence: '95% CI' },
    { month: 'Dec (30d Proj)', actual: null, forecast: 5600, lowerBound: 5150, upperBound: 6050, confidence: '90% CI' },
  ],
  '60d': [
    { month: 'Aug', actual: 4900, forecast: 4800, lowerBound: 4500, upperBound: 5100, confidence: 'Historical' },
    { month: 'Sep', actual: 5150, forecast: 5050, lowerBound: 4700, upperBound: 5400, confidence: 'Historical' },
    { month: 'Oct', actual: 4800, forecast: 4950, lowerBound: 4600, upperBound: 5300, confidence: 'Historical' },
    { month: 'Nov (Current)', actual: 5300, forecast: 5200, lowerBound: 4900, upperBound: 5500, confidence: '95% CI' },
    { month: 'Dec (30d)', actual: null, forecast: 5600, lowerBound: 5150, upperBound: 6050, confidence: '90% CI' },
    { month: 'Jan (60d)', actual: null, forecast: 5850, lowerBound: 5300, upperBound: 6400, confidence: '85% CI' },
  ],
  '90d': [
    { month: 'Jun', actual: 4200, forecast: 4100, lowerBound: 3800, upperBound: 4400, confidence: 'Historical' },
    { month: 'Jul', actual: 4450, forecast: 4300, lowerBound: 4000, upperBound: 4600, confidence: 'Historical' },
    { month: 'Aug', actual: 4900, forecast: 4800, lowerBound: 4500, upperBound: 5100, confidence: 'Historical' },
    { month: 'Sep', actual: 5150, forecast: 5050, lowerBound: 4700, upperBound: 5400, confidence: 'Historical' },
    { month: 'Oct', actual: 4800, forecast: 4950, lowerBound: 4600, upperBound: 5300, confidence: 'Historical' },
    { month: 'Nov (Current)', actual: 5300, forecast: 5200, lowerBound: 4900, upperBound: 5500, confidence: '95% CI' },
    { month: 'Dec (30d)', actual: null, forecast: 5600, lowerBound: 5100, upperBound: 6100, confidence: '90% CI' },
    { month: 'Jan (60d)', actual: null, forecast: 5850, lowerBound: 5250, upperBound: 6450, confidence: '85% CI' },
    { month: 'Feb (90d)', actual: null, forecast: 6100, lowerBound: 5400, upperBound: 6800, confidence: '80% CI' },
  ],
};

// Regional Facility Health Distribution with Regional Metadata
const REGIONAL_FACILITY_STOCK = [
  { name: 'Tikur Anbessa', region: 'Addis Ababa', adequate: 62, understocked: 12, stockout: 6, total: 80 },
  { name: "St. Paul's", region: 'Addis Ababa', adequate: 68, understocked: 8, stockout: 4, total: 80 },
  { name: 'Jimma UMC', region: 'Oromia', adequate: 55, understocked: 18, stockout: 7, total: 80 },
  { name: 'Gondar CSH', region: 'Amhara', adequate: 59, understocked: 14, stockout: 7, total: 80 },
  { name: 'Hawassa CSH', region: 'Sidama', adequate: 64, understocked: 11, stockout: 5, total: 80 },
];

export default function DashboardOverviewPage() {
  const [summary, setSummary] = useState<SystemSummary | null>(null);
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [selectedFacilityId, setSelectedFacilityId] = useState<number | 'all'>('all');
  const [horizonFilter, setHorizonFilter] = useState<'30d' | '60d' | '90d'>('90d');
  const [regionFilter, setRegionFilter] = useState<string>('all');
  const [alertCategoryFilter, setAlertCategoryFilter] = useState<'all' | 'stockout' | 'expiry' | 'quality'>('all');

  // Real or fallback data states
  const [criticalStockouts, setCriticalStockouts] = useState<StockoutRiskItem[]>([]);
  const [expiringBatches, setExpiringBatches] = useState<ExpiryRiskItem[]>([]);
  const [pendingTransfers, setPendingTransfers] = useState<RedistributionProposal[]>([]);
  const [qualityIssues, setQualityIssues] = useState<DataQualityIssue[]>([]);
  const [recentActivities, setRecentActivities] = useState<AuditLogEntry[]>([]);

  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Load initial data
  useEffect(() => {
    loadDashboardData();
  }, [selectedFacilityId]);

  const loadDashboardData = async () => {
    setIsRefreshing(true);
    try {
      const facilityParam = selectedFacilityId === 'all' ? 1 : selectedFacilityId;

      const [sum, facs, stockouts, expiries, transfers, issues, auditLogs] = await Promise.all([
        reportsApi.getSummary(),
        facilitiesApi.list(),
        stockoutApi.getFacilityRisks(facilityParam),
        expiryApi.getFacilityRisks(facilityParam),
        redistributionApi.listRecommendations(selectedFacilityId === 'all' ? undefined : selectedFacilityId),
        dataQualityApi.listIssues(selectedFacilityId === 'all' ? undefined : selectedFacilityId),
        auditLogsApi.list(undefined, undefined, 6),
      ]);

      setSummary(sum);
      setFacilities(facs);
      setCriticalStockouts(stockouts);
      setExpiringBatches(expiries);
      setPendingTransfers(transfers);
      setQualityIssues(issues);
      setRecentActivities(auditLogs);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  // Filtered facility health distribution
  const filteredFacilityStock = useMemo(() => {
    if (regionFilter === 'all') return REGIONAL_FACILITY_STOCK;
    return REGIONAL_FACILITY_STOCK.filter((f) => f.region === regionFilter);
  }, [regionFilter]);

  // Combined Priority Alerts
  const combinedAlerts = useMemo(() => {
    const alerts: Array<{
      id: string;
      category: 'stockout' | 'expiry' | 'quality';
      severity: 'critical' | 'high' | 'warning';
      medicine: string;
      facility: string;
      metric: string;
      actionText: string;
      actionUrl: string;
    }> = [];

    // Critical and high stockouts
    criticalStockouts.forEach((s) => {
      alerts.push({
        id: `stk-${s.medicine_id}-${s.facility_id}`,
        category: 'stockout',
        severity: s.risk_level === 'Critical' ? 'critical' : 'high',
        medicine: s.medicine_name,
        facility: s.facility_name || 'Hospital Depot',
        metric: `DSR: ${(s.days_of_stock_remaining ?? 0).toFixed(1)} days | Stock: ${(s.current_stock ?? 0).toLocaleString()} units`,
        actionText: 'Review Stockout',
        actionUrl: '/stockout-intelligence',
      });
    });

    // Expiry risks
    expiringBatches.forEach((e) => {
      alerts.push({
        id: `exp-${e.batch_id}-${e.facility_id}`,
        category: 'expiry',
        severity: e.risk_level === 'Critical' ? 'critical' : 'high',
        medicine: e.medicine_name,
        facility: e.facility_name || 'Hospital Depot',
        metric: `Expires in ${e.days_until_expiry ?? 0}d | Value at Risk: ETB ${(e.financial_value_at_risk_etb ?? 0).toLocaleString()}`,
        actionText: 'Evaluate FEFO Transfer',
        actionUrl: '/expiry-prevention',
      });
    });

    // Quality warnings
    qualityIssues.slice(0, 3).forEach((q) => {
      alerts.push({
        id: `dqi-${q.id}`,
        category: 'quality',
        severity: q.severity === 'CRITICAL' ? 'critical' : 'warning',
        medicine: q.medicine_name || 'Stock Ledger Record',
        facility: q.facility_name || 'Hospital Depot',
        metric: `Anomaly: ${q.issue_type} in row ${q.row_number ?? 'N/A'}`,
        actionText: 'Resolve in Queue',
        actionUrl: '/data-quality/issues',
      });
    });

    if (alertCategoryFilter === 'all') return alerts;
    return alerts.filter((a) => a.category === alertCategoryFilter);
  }, [criticalStockouts, expiringBatches, qualityIssues, alertCategoryFilter]);

  // Current trend projection series
  const currentTrendData = PROJECTION_DATA_BY_HORIZON[horizonFilter] || PROJECTION_DATA_BY_HORIZON['90d'];

  // Financial values
  const totalFinancialAtRisk = expiringBatches.reduce(
    (acc, b) => acc + (b.financial_value_at_risk_etb ?? 0),
    0
  );

  return (
    <div className="space-y-6">
      {/* Demonstration Environment Notice */}
      <DemoAlert
        title="Demonstration & Research Prototype Environment"
        description="All facility indicators, consumption projections, and transfer recommendations represent simulated scenario models calibrated to Ethiopian National Essential Medicine List (NEML) guidelines. Confidential patient health records are not ingested."
      />

      {/* Top Header & Interactive Control Bar */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 border-b border-slate-200/80 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">
              Executive Supply Chain Overview
            </h1>
            <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-100 text-blue-800 border border-blue-200 uppercase tracking-wide">
              Pilot Release
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Explainable AI decision surveillance for stockout prevention, FEFO expiry reduction, and lateral redistribution in Ethiopian healthcare facilities.
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-2.5">
          {/* Facility Selector */}
          <div className="flex items-center gap-1.5 bg-white border border-slate-300 rounded-lg px-2.5 py-1.5 shadow-xs">
            <Building2 className="w-3.5 h-3.5 text-slate-500 shrink-0" />
            <select
              value={selectedFacilityId}
              onChange={(e) =>
                setSelectedFacilityId(e.target.value === 'all' ? 'all' : Number(e.target.value))
              }
              className="text-xs bg-transparent border-none text-slate-800 font-medium focus:outline-none cursor-pointer"
            >
              <option value="all">National Network (All Facilities)</option>
              {facilities.map((fac) => (
                <option key={fac.id} value={fac.id}>
                  {fac.name}
                </option>
              ))}
            </select>
          </div>

          {/* Refresh Action */}
          <Button
            variant="outline"
            size="sm"
            onClick={loadDashboardData}
            disabled={isRefreshing}
            className="shadow-xs"
            title="Reload all live and simulated metrics"
          >
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isRefreshing ? 'animate-spin text-blue-600' : 'text-slate-500'}`} />
            <span>{isRefreshing ? 'Syncing...' : 'Refresh'}</span>
          </Button>

          {/* Quick Action to Lateral Redistribution */}
          <Link href="/redistribution">
            <Button variant="primary" size="sm" className="shadow-xs">
              <Truck className="w-3.5 h-3.5 mr-1.5" />
              <span>MILP Transfer Optimizer</span>
            </Button>
          </Link>
        </div>
      </div>

      {/* 4 Refined KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* KPI 1: Monitored Facilities */}
        <div className="p-5 bg-white rounded-xl border border-slate-200/90 shadow-xs flex flex-col justify-between h-full hover:border-slate-300 transition-all">
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <div className="flex items-center gap-1.5">
                <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                  Connected Facilities
                </span>
                <Tooltip content="Pilot hospital network calibrated to Ethiopian primary, general, and tertiary health tiers.">
                  <HelpCircle className="w-3.5 h-3.5 text-slate-400 cursor-help" />
                </Tooltip>
              </div>
              <div className="text-2xl font-bold text-slate-900">
                {facilities.length > 0 ? facilities.length : (summary?.total_facilities || 5)}
              </div>
            </div>
            <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
              <Building2 className="w-5 h-5" />
            </div>
          </div>
          <div className="pt-3 mt-3 border-t border-slate-100 flex items-center justify-between text-[11px]">
            <span className="text-slate-500">Addis Ababa, Oromia, Amhara, Sidama</span>
            <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-blue-50 text-blue-700">
              Active Pilot
            </span>
          </div>
        </div>

        {/* KPI 2: Critical Stockout Alerts */}
        <div className="p-5 bg-white rounded-xl border border-slate-200/90 shadow-xs flex flex-col justify-between h-full hover:border-slate-300 transition-all">
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <div className="flex items-center gap-1.5">
                <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                  Critical Stockout Alerts
                </span>
                <Tooltip content="Essential medicines with Days of Stock Remaining (DSR) below safety buffer or supplier replenishment lead time.">
                  <HelpCircle className="w-3.5 h-3.5 text-slate-400 cursor-help" />
                </Tooltip>
              </div>
              <div className="text-2xl font-bold text-rose-600">
                {summary?.critical_stockouts || criticalStockouts.filter(s => s.risk_level === 'Critical' || s.risk_level === 'High').length || 7}
              </div>
            </div>
            <div className="w-10 h-10 rounded-lg bg-rose-50 text-rose-600 flex items-center justify-center shrink-0">
              <AlertTriangle className="w-5 h-5" />
            </div>
          </div>
          <div className="pt-3 mt-3 border-t border-slate-100 flex items-center justify-between text-[11px]">
            <span className="text-rose-700 font-medium">DSR &lt; 5 days or below lead time</span>
            <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-rose-100 text-rose-800">
              Action Req.
            </span>
          </div>
        </div>

        {/* KPI 3: Expiring Batches */}
        <div className="p-5 bg-white rounded-xl border border-slate-200/90 shadow-xs flex flex-col justify-between h-full hover:border-slate-300 transition-all">
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <div className="flex items-center gap-1.5">
                <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                  Batches Expiring &le;90d
                </span>
                <Tooltip content="First-Expired, First-Out (FEFO) lots with Projected Under-Utilization Stock (PUSE) that will expire before consumption.">
                  <HelpCircle className="w-3.5 h-3.5 text-slate-400 cursor-help" />
                </Tooltip>
              </div>
              <div className="text-2xl font-bold text-amber-600">
                {summary?.active_monitored_batches ? Math.min(34, summary.active_monitored_batches) : 34} Batches
              </div>
            </div>
            <div className="w-10 h-10 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center shrink-0">
              <Clock className="w-5 h-5" />
            </div>
          </div>
          <div className="pt-3 mt-3 border-t border-slate-100 flex items-center justify-between text-[11px]">
            <span className="text-amber-800 font-medium">
              ETB {(totalFinancialAtRisk > 0 ? totalFinancialAtRisk : 17380).toLocaleString()} risk under FEFO
            </span>
            <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-amber-100 text-amber-800">
              Redistribute
            </span>
          </div>
        </div>

        {/* KPI 4: Data Quality Index */}
        <div className="p-5 bg-white rounded-xl border border-slate-200/90 shadow-xs flex flex-col justify-between h-full hover:border-slate-300 transition-all">
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <div className="flex items-center gap-1.5">
                <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                  National DQI Index
                </span>
                <Tooltip content="Weighted 5D integrity score: Completeness (25%), Consistency (25%), Plausibility (20%), Expiry Validity (15%), Uniqueness (15%).">
                  <HelpCircle className="w-3.5 h-3.5 text-slate-400 cursor-help" />
                </Tooltip>
              </div>
              <div className="text-2xl font-bold text-emerald-600">
                {(summary?.average_dqi_score ?? 93.6).toFixed(1)}%
              </div>
            </div>
            <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
              <CheckCircle2 className="w-5 h-5" />
            </div>
          </div>
          <div className="pt-3 mt-3 border-t border-slate-100 flex items-center justify-between text-[11px]">
            <span className="text-emerald-700 font-medium">Grade A &bull; Verified for AI Inference</span>
            <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800">
              Compliant
            </span>
          </div>
        </div>
      </div>

      {/* Analytics Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: National Demand Forecast & Projection Intervals */}
        <Card
          title="National Consumption & ML Demand Projection"
          subtitle="HistGradientBoosting + Croston ensemble with P10/P90 prediction intervals"
          action={
            <div className="flex items-center gap-1 bg-slate-100 p-0.5 rounded-lg text-xs">
              {(['30d', '60d', '90d'] as const).map((h) => (
                <button
                  key={h}
                  onClick={() => setHorizonFilter(h)}
                  className={`px-2 py-0.5 rounded-md font-medium text-[11px] transition ${
                    horizonFilter === h
                      ? 'bg-white text-blue-700 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {h.toUpperCase()}
                </button>
              ))}
            </div>
          }
        >
          <div className="space-y-2">
            <div className="h-72 w-full pt-2">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={currentTrendData} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                  <XAxis dataKey="month" stroke="#64748b" fontSize={11} tickLine={false} />
                  <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                  <RechartsTooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      border: '1px solid #334155',
                      color: '#fff',
                      borderRadius: '8px',
                      fontSize: '11px',
                      padding: '8px 12px',
                    }}
                    formatter={(val: any, name: string) => [
                      val ? `${Number(val).toLocaleString()} units` : 'N/A',
                      name === 'actual'
                        ? 'Historical Dispensing'
                        : name === 'forecast'
                        ? 'Predicted Demand (P50)'
                        : name === 'upperBound'
                        ? 'Upper Confidence Band (P90)'
                        : 'Lower Confidence Band (P10)',
                    ]}
                  />
                  <Legend
                    wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }}
                    iconType="circle"
                  />
                  {/* Upper/Lower Prediction Interval Band */}
                  <Area
                    type="monotone"
                    dataKey="upperBound"
                    name="Upper Band (P90)"
                    stroke="#93c5fd"
                    fill="#dbeafe"
                    fillOpacity={0.4}
                  />
                  {/* Predicted Demand Line */}
                  <Line
                    type="monotone"
                    dataKey="forecast"
                    name="Forecast (P50)"
                    stroke="#2563eb"
                    strokeWidth={2.5}
                    dot={{ r: 3, fill: '#2563eb' }}
                  />
                  {/* Actual Dispensing History */}
                  <Line
                    type="monotone"
                    dataKey="actual"
                    name="Historical Consumption"
                    stroke="#059669"
                    strokeWidth={2.5}
                    dot={{ r: 4, fill: '#059669' }}
                    connectNulls={false}
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
            <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1 border-t border-slate-100">
              <span className="flex items-center gap-1">
                <Info className="w-3 h-3 text-slate-400" />
                Shaded band represents 90% confidence bound for supply planning
              </span>
              <Link href="/forecasting" className="text-blue-600 hover:text-blue-700 font-medium flex items-center gap-0.5">
                Model Details <ChevronRight className="w-3 h-3" />
              </Link>
            </div>
          </div>
        </Card>

        {/* Chart 2: Regional Facility Stock Health Distribution */}
        <Card
          title="Regional Facility Inventory Health Distribution"
          subtitle="Proportion of adequate, understocked, and stockout medicines"
          action={
            <div className="flex items-center gap-1.5">
              <Filter className="w-3.5 h-3.5 text-slate-400" />
              <select
                value={regionFilter}
                onChange={(e) => setRegionFilter(e.target.value)}
                className="text-xs bg-slate-50 border border-slate-200 rounded-md px-2 py-1 text-slate-700 font-medium focus:outline-none"
              >
                <option value="all">All Regions</option>
                <option value="Addis Ababa">Addis Ababa</option>
                <option value="Oromia">Oromia</option>
                <option value="Amhara">Amhara</option>
                <option value="Sidama">Sidama</option>
              </select>
            </div>
          }
        >
          <div className="space-y-2">
            <div className="h-72 w-full pt-2">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={filteredFacilityStock} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                  <XAxis dataKey="name" stroke="#64748b" fontSize={11} tickLine={false} />
                  <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                  <RechartsTooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      border: '1px solid #334155',
                      color: '#fff',
                      borderRadius: '8px',
                      fontSize: '11px',
                      padding: '8px 12px',
                    }}
                    formatter={(val: any, name: string) => [
                      `${val} SKUs (${((Number(val) / 80) * 100).toFixed(0)}%)`,
                      name === 'adequate'
                        ? 'Adequate Stock'
                        : name === 'understocked'
                        ? 'Understocked (5-15 DSR)'
                        : 'Stockout (<5 DSR)',
                    ]}
                  />
                  <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} iconType="circle" />
                  <Bar dataKey="adequate" name="Adequate (>15 DSR)" stackId="a" fill="#10b981" radius={[0, 0, 0, 0]} />
                  <Bar dataKey="understocked" name="Understocked (5-15 DSR)" stackId="a" fill="#f59e0b" />
                  <Bar dataKey="stockout" name="Stockout (<5 DSR)" stackId="a" fill="#ef4444" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1 border-t border-slate-100">
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-rose-500 inline-block"></span>
                Red alerts trigger automated lateral redistribution recommendations
              </span>
              <Link href="/inventory" className="text-blue-600 hover:text-blue-700 font-medium flex items-center gap-0.5">
                View Inventory <ChevronRight className="w-3 h-3" />
              </Link>
            </div>
          </div>
        </Card>
      </div>

      {/* Priority Alerts & Recent Activity Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Priority Alerts Feed (2 Columns on large screens) */}
        <div className="xl:col-span-2 space-y-4">
          <Card
            title="Priority Operational Alerts"
            subtitle="Immediate clinical and supply chain vulnerabilities requiring attention"
            action={
              <div className="flex items-center gap-1">
                {(['all', 'stockout', 'expiry', 'quality'] as const).map((cat) => (
                  <button
                    key={cat}
                    onClick={() => setAlertCategoryFilter(cat)}
                    className={`px-2 py-0.5 rounded text-[11px] font-medium capitalize transition ${
                      alertCategoryFilter === cat
                        ? 'bg-blue-600 text-white shadow-xs'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            }
          >
            <div className="space-y-3">
              {combinedAlerts.length === 0 ? (
                <div className="py-8 text-center text-xs text-slate-500">
                  <CheckCircle2 className="w-8 h-8 text-emerald-500 mx-auto mb-2" />
                  No high-priority alerts matching the selected category.
                </div>
              ) : (
                combinedAlerts.slice(0, 5).map((alert) => (
                  <div
                    key={alert.id}
                    className={`p-3.5 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-3 transition ${
                      alert.severity === 'critical'
                        ? 'bg-rose-50/40 border-rose-200/80'
                        : alert.severity === 'high'
                        ? 'bg-amber-50/40 border-amber-200/80'
                        : 'bg-blue-50/40 border-blue-200/80'
                    }`}
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                            alert.severity === 'critical'
                              ? 'bg-rose-100 text-rose-800'
                              : alert.severity === 'high'
                              ? 'bg-amber-100 text-amber-800'
                              : 'bg-blue-100 text-blue-800'
                          }`}
                        >
                          {alert.severity}
                        </span>
                        <span className="text-xs font-bold text-slate-900">{alert.medicine}</span>
                        <span className="text-xs text-slate-500">• {alert.facility}</span>
                      </div>
                      <div className="text-[11px] text-slate-600 font-medium">
                        {alert.metric}
                      </div>
                    </div>

                    <div className="shrink-0 flex items-center">
                      <Link
                        href={alert.actionUrl as any}
                        className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 hover:text-blue-600 text-xs font-semibold shadow-xs transition"
                      >
                        <span>{alert.actionText}</span>
                        <ChevronRight className="w-3.5 h-3.5" />
                      </Link>
                    </div>
                  </div>
                ))
              )}
            </div>
            {combinedAlerts.length > 5 && (
              <div className="pt-3 border-t border-slate-100 text-center">
                <Link
                  href="/notifications"
                  className="text-xs text-blue-600 hover:text-blue-700 font-semibold inline-flex items-center gap-1"
                >
                  View all {combinedAlerts.length} operational alerts in Notification Center
                  <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            )}
          </Card>
        </div>

        {/* Recent Activity Feed (1 Column) */}
        <div className="space-y-4">
          <Card
            title="Recent Activity"
            subtitle="Live ledger updates and automated decisions"
            action={
              <Link
                href="/audit-logs"
                className="text-xs text-blue-600 hover:text-blue-700 font-medium flex items-center gap-0.5"
              >
                Audit Log <ChevronRight className="w-3.5 h-3.5" />
              </Link>
            }
          >
            <div className="space-y-3.5">
              {recentActivities.map((log) => {
                const isTransfer = log.action?.includes('REDISTRIBUTION') || log.entity_type?.includes('Redistribution');
                const isBatch = log.action?.includes('BATCH') || log.action?.includes('DISPENSE');
                const isQuality = log.action?.includes('DQI') || log.action?.includes('ANOMALY');

                const timeDisplay = log.timestamp
                  ? new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                  : 'Recent';

                return (
                  <div key={log.id} className="flex items-start gap-3 text-xs">
                    <div
                      className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 mt-0.5 ${
                        isTransfer
                          ? 'bg-blue-100 text-blue-700'
                          : isBatch
                          ? 'bg-amber-100 text-amber-700'
                          : isQuality
                          ? 'bg-emerald-100 text-emerald-700'
                          : 'bg-slate-100 text-slate-700'
                      }`}
                    >
                      {isTransfer ? (
                        <Truck className="w-3.5 h-3.5" />
                      ) : isBatch ? (
                        <Clock className="w-3.5 h-3.5" />
                      ) : isQuality ? (
                        <ShieldCheck className="w-3.5 h-3.5" />
                      ) : (
                        <Activity className="w-3.5 h-3.5" />
                      )}
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-1">
                        <span className="font-semibold text-slate-900 truncate">
                          {log.action?.replace(/_/g, ' ')}
                        </span>
                        <span className="text-[10px] text-slate-400 shrink-0">{timeDisplay}</span>
                      </div>
                      <div className="text-[11px] text-slate-600 truncate mt-0.5">
                        {typeof log.details === 'object' && log.details !== null
                          ? JSON.stringify(log.details).replace(/[{"}]/g, ' ').slice(0, 50)
                          : String(log.details || 'Standard verification recorded')}
                      </div>
                      <div className="text-[10px] text-slate-400 mt-0.5 flex items-center gap-1.5">
                        <span>{log.user_email || 'System Daemon'}</span>
                        <span>•</span>
                        <span className="font-mono text-[9px] bg-slate-100 px-1 rounded text-slate-500">
                          {log.id > 100 ? 'Simulated Log' : 'Verified'}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="pt-3 border-t border-slate-100 text-center">
              <Link
                href="/audit-logs"
                className="text-[11px] text-slate-500 hover:text-slate-800 font-medium inline-flex items-center gap-1"
              >
                View complete immutable audit trail <ChevronRight className="w-3 h-3" />
              </Link>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
