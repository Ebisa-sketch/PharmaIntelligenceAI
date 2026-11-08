'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { expiryApi, facilitiesApi } from '@/lib/api';
import { ExpiryRiskItem, Facility } from '@/types';
import {
  Clock,
  AlertTriangle,
  RefreshCw,
  Search,
  DollarSign,
  TrendingDown,
  Layers,
  ArrowRight,
  ShieldCheck,
} from 'lucide-react';
import Link from 'next/link';

export default function ExpiryPreventionPage() {
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<number>(1);
  const [selectedRiskLevel, setSelectedRiskLevel] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [expiryRisks, setExpiryRisks] = useState<ExpiryRiskItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

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
    async function loadExpiry() {
      setIsLoading(true);
      try {
        const data = await expiryApi.getFacilityRisks(
          selectedFacility,
          selectedRiskLevel === 'All' ? undefined : selectedRiskLevel
        );
        setExpiryRisks(data);
      } catch (err) {
        console.error('Failed to load expiry risks:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadExpiry();
  }, [selectedFacility, selectedRiskLevel]);

  const filteredItems = expiryRisks.filter((item) => {
    const q = searchQuery.toLowerCase();
    return (
      item.medicine_name.toLowerCase().includes(q) ||
      item.batch_number.toLowerCase().includes(q)
    );
  });

  const totalValueAtRisk = expiryRisks.reduce(
    (sum, item) => sum + (item.financial_value_at_risk_etb ?? 0),
    0
  );

  const totalUnusedUnits = expiryRisks.reduce(
    (sum, item) => sum + (item.projected_unused_stock ?? 0),
    0
  );

  const getRiskBadge = (level: string) => {
    switch (level) {
      case 'Critical':
        return <Badge variant="danger">Critical (&lt;30d)</Badge>;
      case 'High':
        return <Badge variant="warning">High Risk (&lt;90d)</Badge>;
      case 'Medium':
        return <Badge variant="info">Medium</Badge>;
      default:
        return <Badge variant="success">Safe</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Expiry Prevention &amp; FEFO Queue Optimization
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Simulates consumption burn-down under FEFO to forecast Projected Unused Stock at Expiry (PUSE) and financial loss.
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
            placeholder="Search batch or medicine..."
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
            <option value="All">All Expiry Horizons</option>
            <option value="Critical">Critical (&lt;30 Days)</option>
            <option value="High">High Risk (&lt;90 Days)</option>
            <option value="Medium">Medium (90-180 Days)</option>
          </select>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Total Financial Loss at Risk
          </div>
          <div className="text-2xl font-bold text-rose-600 mt-1">
            {totalValueAtRisk.toLocaleString()} ETB
          </div>
          <div className="text-[11px] text-rose-700 mt-0.5">
            Without lateral redistribution
          </div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Projected Unused Stock (PUSE)
          </div>
          <div className="text-2xl font-bold text-amber-600 mt-1">
            {totalUnusedUnits.toLocaleString()} units
          </div>
          <div className="text-[11px] text-amber-700 mt-0.5">
            Surplus across monitored batches
          </div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Batches at Risk
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-1">
            {expiryRisks.length} Batches
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">
            In First-Expired queue
          </div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Average Shelf Life Left
          </div>
          <div className="text-2xl font-bold text-blue-600 mt-1">
            42.8 Days
          </div>
          <div className="text-[11px] text-blue-700 mt-0.5">
            Sufficient for regional transit
          </div>
        </div>
      </div>

      {/* Expiry Risk Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
              <tr>
                <th className="px-6 py-3.5">Batch / Medicine</th>
                <th className="px-6 py-3.5">Current Stock</th>
                <th className="px-6 py-3.5">Unit Cost (ETB)</th>
                <th className="px-6 py-3.5">Expiry Date</th>
                <th className="px-6 py-3.5">Days Left</th>
                <th className="px-6 py-3.5">PUSE (Surplus)</th>
                <th className="px-6 py-3.5">Loss at Risk (ETB)</th>
                <th className="px-6 py-3.5">Status</th>
                <th className="px-6 py-3.5 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredItems.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50/60 transition-colors">
                  <td className="px-6 py-3.5">
                    <div className="font-semibold text-slate-900">{item.medicine_name}</div>
                    <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                      Batch: {item.batch_number}
                    </div>
                  </td>
                  <td className="px-6 py-3.5 font-bold text-slate-900">
                    {(item.current_quantity ?? 0).toLocaleString()}
                  </td>
                  <td className="px-6 py-3.5 text-slate-700 font-medium">
                    {(item.unit_cost ?? 0).toFixed(2)} ETB
                  </td>
                  <td className="px-6 py-3.5 font-mono text-slate-600">
                    {item.expiry_date}
                  </td>
                  <td className="px-6 py-3.5 font-bold">
                    <span className={(item.days_until_expiry ?? 0) <= 30 ? 'text-rose-600' : 'text-amber-600'}>
                      {item.days_until_expiry ?? 0} days
                    </span>
                  </td>
                  <td className="px-6 py-3.5 font-semibold text-amber-700">
                    {(item.projected_unused_stock ?? 0).toLocaleString()} units
                  </td>
                  <td className="px-6 py-3.5 font-bold text-rose-600">
                    {(item.financial_value_at_risk_etb ?? 0).toLocaleString()} ETB
                  </td>
                  <td className="px-6 py-3.5">{getRiskBadge(item.risk_level)}</td>
                  <td className="px-6 py-3.5 text-right">
                    <Link href="/redistribution">
                      <Button variant="outline" size="sm">
                        Redistribute &rarr;
                      </Button>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
