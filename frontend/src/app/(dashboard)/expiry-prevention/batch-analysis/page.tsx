'use client';

import { useState, useEffect } from 'react';
import { 
  Clock, 
  AlertTriangle, 
  AlertCircle, 
  ShieldCheck, 
  Search, 
  Filter, 
  Calendar, 
  RefreshCw,
  Coins
} from 'lucide-react';
import { batchesApi, facilitiesApi } from '@/lib/api';
import { BatchItem, Facility } from '@/types';
import DemoAlert from '@/components/ui/DemoAlert';
import Pagination from '@/components/ui/Pagination';
import EmptyState from '@/components/ui/EmptyState';

export default function ExpiryBatchAnalysisPage() {
  const [batches, setBatches] = useState<BatchItem[]>([]);
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<number | 'all'>('all');
  const [shelfLifeFilter, setShelfLifeFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;

  useEffect(() => {
    loadData();
  }, [selectedFacility]);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [facs, batchData] = await Promise.all([
        facilitiesApi.list(),
        batchesApi.list(selectedFacility === 'all' ? undefined : selectedFacility),
      ]);
      setFacilities(facs);
      setBatches(batchData);
    } catch {
      // Fallback in API
    } finally {
      setIsLoading(false);
    }
  };

  const filteredBatches = batches.filter(batch => {
    const term = searchQuery.toLowerCase();
    const batchMatch = (batch.batch_number ?? '').toLowerCase().includes(term);
    const medMatch = (batch.medicine_name ?? '').toLowerCase().includes(term);
    const facMatch = (batch.facility_name ?? '').toLowerCase().includes(term);
    if (!batchMatch && !medMatch && !facMatch) return false;

    const days = batch.days_to_expiry ?? 0;
    if (shelfLifeFilter === 'critical' && days > 30) return false;
    if (shelfLifeFilter === 'moderate' && (days <= 30 || days > 90)) return false;
    if (shelfLifeFilter === 'healthy' && days <= 90) return false;

    return true;
  });

  const totalPages = Math.ceil(filteredBatches.length / pageSize) || 1;
  const paginatedBatches = filteredBatches.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  const criticalBatches = batches.filter(b => (b.days_to_expiry ?? 0) <= 30);
  const moderateBatches = batches.filter(b => (b.days_to_expiry ?? 0) > 30 && (b.days_to_expiry ?? 0) <= 90);
  const totalValueAtRisk = batches
    .filter(b => (b.days_to_expiry ?? 0) <= 90)
    .reduce((acc, b) => acc + (b.current_quantity ?? 0) * (b.unit_cost ?? 0), 0);

  return (
    <div className="space-y-6">
      <DemoAlert 
        title="FEFO Batch Expiry & Depletion Velocity Inspector"
        description="First-Expired, First-Out (FEFO) batch tracking evaluating burn rate against remaining shelf life to identify Projected Under-Utilization (PUSE) and prevent physical medicine expiration."
      />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Batch-Level Expiry Analysis</h1>
          <p className="text-sm text-slate-500 mt-1">
            Granular lot intelligence inspecting active pharmaceutical inventory batches across hospital storage depots.
          </p>
        </div>
        <button
          onClick={loadData}
          disabled={isLoading}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-300 bg-white text-xs font-medium text-slate-700 hover:bg-slate-50 shadow-sm transition"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-slate-500 ${isLoading ? 'animate-spin' : ''}`} />
          Refresh Batches
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Critical Batches (&le; 30 Days)</span>
            <AlertCircle className="w-4 h-4 text-rose-600" />
          </div>
          <div className="text-2xl font-bold text-rose-600 mt-2">{criticalBatches.length} Batches</div>
          <div className="text-xs text-rose-700 mt-1">Requires emergency transfer or fast-track dispensing</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Moderate Watch (31-90 Days)</span>
            <AlertTriangle className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-amber-600 mt-2">{moderateBatches.length} Batches</div>
          <div className="text-xs text-amber-700 mt-1">Scheduled for regional redistribution review</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Near-Expiry Value at Risk</span>
            <Coins className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-2">
            ETB {totalValueAtRisk.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </div>
          <div className="text-xs text-slate-500 mt-1">Financial value of stock expiring within 90 days</div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search by lot number, medicine name, or facility..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          />
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={selectedFacility}
              onChange={(e) => setSelectedFacility(e.target.value === 'all' ? 'all' : Number(e.target.value))}
              className="text-xs border border-slate-300 rounded-lg px-2.5 py-1.5 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Facilities</option>
              {facilities.map(f => (
                <option key={f.id} value={f.id}>{f.name}</option>
              ))}
            </select>
          </div>

          <select
            value={shelfLifeFilter}
            onChange={(e) => setShelfLifeFilter(e.target.value)}
            className="text-xs border border-slate-300 rounded-lg px-2.5 py-1.5 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Expiry Windows</option>
            <option value="critical">&le; 30 Days (Critical)</option>
            <option value="moderate">31 - 90 Days (Warning)</option>
            <option value="healthy">&gt; 90 Days (Healthy)</option>
          </select>
        </div>
      </div>

      {/* Batches Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-50 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="px-4 py-3">Batch Lot #</th>
                <th className="px-4 py-3">Medicine</th>
                <th className="px-4 py-3">Facility</th>
                <th className="px-4 py-3">Expiry Date</th>
                <th className="px-4 py-3 text-center">Remaining Days</th>
                <th className="px-4 py-3 text-right">Current Stock</th>
                <th className="px-4 py-3 text-right">Value (ETB)</th>
                <th className="px-4 py-3">FEFO Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {paginatedBatches.length === 0 ? (
                <tr>
                  <td colSpan={8} className="px-4 py-12 text-center text-slate-500">
                    <EmptyState
                      title="No Batches Match Selection"
                      description="Try adjusting your facility filter or search query."
                    />
                  </td>
                </tr>
              ) : (
                paginatedBatches.map((batch) => {
                  const days = batch.days_to_expiry ?? 0;
                  const value = (batch.current_quantity ?? 0) * (batch.unit_cost ?? 0);
                  return (
                    <tr key={batch.id} className="hover:bg-slate-50/80 transition">
                      <td className="px-4 py-3.5 font-mono font-medium text-slate-900">
                        {batch.batch_number}
                      </td>
                      <td className="px-4 py-3.5 font-medium text-slate-800">
                        {batch.medicine_name}
                      </td>
                      <td className="px-4 py-3.5 text-slate-600">
                        {batch.facility_name}
                      </td>
                      <td className="px-4 py-3.5 text-slate-600">
                        {batch.expiry_date ? new Date(batch.expiry_date).toLocaleDateString() : 'N/A'}
                      </td>
                      <td className="px-4 py-3.5 text-center font-bold">
                        {days <= 30 ? (
                          <span className="text-rose-600">{days} days</span>
                        ) : days <= 90 ? (
                          <span className="text-amber-600">{days} days</span>
                        ) : (
                          <span className="text-slate-700">{days} days</span>
                        )}
                      </td>
                      <td className="px-4 py-3.5 text-right font-medium text-slate-900">
                        {(batch.current_quantity ?? 0).toLocaleString()}
                      </td>
                      <td className="px-4 py-3.5 text-right text-slate-700">
                        ETB {value.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                      </td>
                      <td className="px-4 py-3.5">
                        {days <= 30 ? (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-semibold bg-rose-100 text-rose-800 border border-rose-200">
                            Critical FEFO
                          </span>
                        ) : days <= 90 ? (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-100 text-amber-800 border border-amber-200">
                            Near Expiry
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                            Valid
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {totalPages > 1 && (
          <div className="p-3 border-t border-slate-200">
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
              totalItems={filteredBatches.length}
              pageSize={pageSize}
            />
          </div>
        )}
      </div>
    </div>
  );
}
