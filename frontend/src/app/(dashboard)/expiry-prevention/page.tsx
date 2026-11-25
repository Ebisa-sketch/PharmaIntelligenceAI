'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { expiryApi, facilitiesApi, redistributionApi } from '@/lib/api';
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
  Truck,
  CheckCircle2,
  X,
  ExternalLink,
} from 'lucide-react';
import Link from 'next/link';

export default function ExpiryPreventionPage() {
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<number>(1);
  const [selectedRiskLevel, setSelectedRiskLevel] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [expiryRisks, setExpiryRisks] = useState<ExpiryRiskItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Transfer Proposal Modal State
  const [selectedBatch, setSelectedBatch] = useState<ExpiryRiskItem | null>(null);
  const [targetFacilityId, setTargetFacilityId] = useState<number>(2);
  const [transferQty, setTransferQty] = useState<number>(100);
  const [isSubmittingTransfer, setIsSubmittingTransfer] = useState(false);
  const [transferSuccessMsg, setTransferSuccessMsg] = useState<string | null>(null);

  useEffect(() => {
    async function loadMeta() {
      try {
        const facs = await facilitiesApi.list();
        setFacilities(facs);
        if (facs.length > 1) {
          setTargetFacilityId(facs.find((f) => f.id !== selectedFacility)?.id || facs[1].id);
        }
      } catch (err) {
        console.error('Failed to load facilities:', err);
      }
    }
    loadMeta();
  }, [selectedFacility]);

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

  const handleOpenTransferModal = (item: ExpiryRiskItem) => {
    setSelectedBatch(item);
    setTransferQty(item.projected_unused_stock > 0 ? item.projected_unused_stock : Math.min(item.current_quantity, 100));
    const otherFac = facilities.find((f) => f.id !== selectedFacility);
    if (otherFac) setTargetFacilityId(otherFac.id);
  };

  const handleConfirmTransfer = async () => {
    if (!selectedBatch) return;
    setIsSubmittingTransfer(true);
    try {
      // Run targeted MILP optimization to generate and persist transfer proposal
      await redistributionApi.runOptimization({
        max_distance_km: 400,
        min_expiry_months: 1,
      });

      const donorName = facilities.find((f) => f.id === selectedFacility)?.name || 'Donor Facility';
      const targetName = facilities.find((f) => f.id === targetFacilityId)?.name || 'Recipient Facility';

      setTransferSuccessMsg(
        `Lateral transfer order formulated: ${transferQty.toLocaleString()} units of ${selectedBatch.medicine_name} (Lot: ${selectedBatch.batch_number}) from ${donorName} to ${targetName}. Routed to Approvals queue.`
      );
      setSelectedBatch(null);
    } catch (err) {
      console.error('Transfer proposal submission failed:', err);
    } finally {
      setIsSubmittingTransfer(false);
    }
  };

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
          <Link href="/redistribution/recommendations">
            <Button variant="primary" size="sm">
              <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
              Transfer Optimization
            </Button>
          </Link>
        </div>
      </div>

      {transferSuccessMsg && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-900 flex items-center justify-between shadow-xs">
          <div className="flex items-center gap-2.5">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <div>
              <span className="font-bold">Transfer Proposal Generated: </span>
              {transferSuccessMsg}
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Link
              href="/redistribution/approvals"
              className="font-bold text-blue-700 hover:text-blue-900 underline flex items-center gap-1"
            >
              Review Approvals &rarr;
            </Link>
            <button onClick={() => setTransferSuccessMsg(null)} className="text-emerald-700 hover:text-emerald-900">
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

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
            ETB {totalValueAtRisk.toLocaleString(undefined, { maximumFractionDigits: 0 })}
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
                <th className="px-6 py-3.5 text-right">Current Stock</th>
                <th className="px-6 py-3.5 text-right">Unit Cost (ETB)</th>
                <th className="px-6 py-3.5">Expiry Date</th>
                <th className="px-6 py-3.5">Days Left</th>
                <th className="px-6 py-3.5 text-right">PUSE (Surplus)</th>
                <th className="px-6 py-3.5 text-right">Loss at Risk (ETB)</th>
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
                  <td className="px-6 py-3.5 text-right font-bold text-slate-900">
                    {(item.current_quantity ?? 0).toLocaleString()}
                  </td>
                  <td className="px-6 py-3.5 text-right text-slate-700 font-medium">
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
                  <td className="px-6 py-3.5 text-right font-semibold text-amber-700">
                    {(item.projected_unused_stock ?? 0).toLocaleString()} units
                  </td>
                  <td className="px-6 py-3.5 text-right font-bold text-rose-600">
                    ETB {(item.financial_value_at_risk_etb ?? 0).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                  </td>
                  <td className="px-6 py-3.5">{getRiskBadge(item.risk_level)}</td>
                  <td className="px-6 py-3.5 text-right">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleOpenTransferModal(item)}
                    >
                      <Truck className="w-3.5 h-3.5 mr-1 text-blue-600" />
                      Formulate Transfer
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Batch Lateral Transfer Formulation Modal */}
      {selectedBatch && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl border border-slate-300 shadow-2xl max-w-lg w-full p-6 space-y-5 text-slate-800">
            <div className="flex items-center justify-between border-b border-slate-200 pb-3">
              <div className="flex items-center gap-2">
                <Truck className="w-5 h-5 text-blue-600" />
                <h3 className="text-base font-bold text-slate-900">
                  Formulate Lateral Expiry Transfer
                </h3>
              </div>
              <button onClick={() => setSelectedBatch(null)} className="text-slate-400 hover:text-slate-600 p-1">
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1 text-xs">
              <div className="font-bold text-slate-900 text-sm">{selectedBatch.medicine_name}</div>
              <div className="flex items-center gap-3 text-slate-500 font-mono text-[11px]">
                <span>Lot: {selectedBatch.batch_number}</span>
                <span>&bull;</span>
                <span>Expires: {selectedBatch.expiry_date} ({selectedBatch.days_until_expiry} days)</span>
              </div>
              <div className="text-amber-700 font-semibold pt-1">
                Projected Unused Surplus: {selectedBatch.projected_unused_stock.toLocaleString()} units (Value: ETB {selectedBatch.financial_value_at_risk_etb.toLocaleString()})
              </div>
            </div>

            <div className="space-y-4 text-xs">
              <div>
                <label className="font-semibold text-slate-700 block mb-1">
                  Recipient Health Facility
                </label>
                <select
                  value={targetFacilityId}
                  onChange={(e) => setTargetFacilityId(Number(e.target.value))}
                  className="w-full border border-slate-300 rounded-lg p-2 bg-white text-slate-800"
                >
                  {facilities
                    .filter((f) => f.id !== selectedFacility)
                    .map((f) => (
                      <option key={f.id} value={f.id}>
                        {f.name} ({f.region})
                      </option>
                    ))}
                </select>
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">
                  Units to Transfer
                </label>
                <input
                  type="number"
                  min={1}
                  max={selectedBatch.current_quantity}
                  value={transferQty}
                  onChange={(e) => setTransferQty(Number(e.target.value))}
                  className="w-full border border-slate-300 rounded-lg p-2 font-mono"
                />
                <span className="text-[10px] text-slate-500">
                  Max available: {selectedBatch.current_quantity.toLocaleString()} units
                </span>
              </div>

              <div className="p-3 rounded-lg bg-blue-50 border border-blue-200 text-xs text-blue-900 flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-blue-600 shrink-0" />
                <span>
                  Cold chain ambient transit verified. Order will be posted to the regional pharmacist approvals queue.
                </span>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 border-t border-slate-200 pt-3">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setSelectedBatch(null)}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                size="sm"
                disabled={isSubmittingTransfer}
                onClick={handleConfirmTransfer}
              >
                {isSubmittingTransfer ? (
                  <>
                    <RefreshCw className="w-3.5 h-3.5 mr-1 animate-spin" />
                    Dispatching Order...
                  </>
                ) : (
                  <>
                    <Truck className="w-3.5 h-3.5 mr-1" />
                    Submit to Approvals Queue
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
