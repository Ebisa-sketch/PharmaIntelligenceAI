'use client';

import { useState, useEffect } from 'react';
import { 
  Network, 
  ArrowRight, 
  Coins, 
  Filter, 
  Search, 
  RefreshCw, 
  CheckCircle2, 
  Sparkles,
  Truck
} from 'lucide-react';
import { redistributionApi, facilitiesApi } from '@/lib/api';
import { RedistributionProposal, Facility } from '@/types';
import DemoAlert from '@/components/ui/DemoAlert';
import Pagination from '@/components/ui/Pagination';
import EmptyState from '@/components/ui/EmptyState';

export default function RedistributionRecommendationsPage() {
  const [proposals, setProposals] = useState<RedistributionProposal[]>([]);
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<number | 'all'>('all');
  const [priorityFilter, setPriorityFilter] = useState<string>('all');
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
      const [facs, props] = await Promise.all([
        facilitiesApi.list(),
        redistributionApi.listRecommendations(selectedFacility === 'all' ? undefined : selectedFacility),
      ]);
      setFacilities(facs);
      setProposals(props);
    } catch {
      // Fallback in API
    } finally {
      setIsLoading(false);
    }
  };

  const filteredProposals = proposals.filter(p => {
    const term = searchQuery.toLowerCase();
    const medMatch = (p.medicine_name ?? '').toLowerCase().includes(term);
    const srcMatch = (p.source_facility_name ?? '').toLowerCase().includes(term);
    const dstMatch = (p.target_facility_name ?? '').toLowerCase().includes(term);
    if (!medMatch && !srcMatch && !dstMatch) return false;

    if (priorityFilter !== 'all' && p.priority !== priorityFilter) return false;

    return true;
  });

  const totalPages = Math.ceil(filteredProposals.length / pageSize) || 1;
  const paginatedProposals = filteredProposals.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  const totalSavedEtb = proposals.reduce((acc, p) => acc + (p.net_value_saved_etb ?? 0), 0);
  const highPriorityCount = proposals.filter(p => p.priority === 'High').length;

  return (
    <div className="space-y-6">
      <DemoAlert 
        title="MILP Route Optimization Recommendations"
        description="Mixed-Integer Linear Programming recommendations minimizing road transfer costs while respecting donor buffer constraints and eliminating recipient stockout risk."
      />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Redistribution Recommendations</h1>
          <p className="text-sm text-slate-500 mt-1">
            Algorithmically generated lateral transfers matching surplus inventory with acute regional stockout deficits.
          </p>
        </div>
        <button
          onClick={loadData}
          disabled={isLoading}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-300 bg-white text-xs font-medium text-slate-700 hover:bg-slate-50 shadow-sm transition"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-slate-500 ${isLoading ? 'animate-spin' : ''}`} />
          Re-evaluate Routes
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>High Priority Transfers</span>
            <Sparkles className="w-4 h-4 text-rose-600" />
          </div>
          <div className="text-2xl font-bold text-rose-600 mt-2">{highPriorityCount} Routes</div>
          <div className="text-xs text-rose-700 mt-1">Immediate shortage avoidance</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Total Value Preserved</span>
            <Coins className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">
            ETB {totalSavedEtb.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </div>
          <div className="text-xs text-emerald-700 mt-1">Net financial savings vs. expiration loss</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Optimization Method</span>
            <Network className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-2">PuLP MILP</div>
          <div className="text-xs text-blue-600 mt-1">Branch-and-Bound Simplex Engine</div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search by medicine, donor facility, or recipient facility..."
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
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="text-xs border border-slate-300 rounded-lg px-2.5 py-1.5 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Priorities</option>
            <option value="High">High Priority</option>
            <option value="Medium">Medium Priority</option>
            <option value="Low">Low Priority</option>
          </select>
        </div>
      </div>

      {/* Proposals Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-50 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="px-4 py-3">Route ID</th>
                <th className="px-4 py-3">Medicine</th>
                <th className="px-4 py-3">Source &rarr; Recipient Route</th>
                <th className="px-4 py-3 text-right">Recommended Qty</th>
                <th className="px-4 py-3 text-right">Distance</th>
                <th className="px-4 py-3 text-right">Net Savings (ETB)</th>
                <th className="px-4 py-3">Priority</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {paginatedProposals.length === 0 ? (
                <tr>
                  <td colSpan={8} className="px-4 py-12 text-center text-slate-500">
                    <EmptyState
                      title="No Recommendations Available"
                      description="No lateral transfers meet current filter parameters or inventory thresholds."
                    />
                  </td>
                </tr>
              ) : (
                paginatedProposals.map((proposal) => (
                  <tr key={proposal.id} className="hover:bg-slate-50/80 transition">
                    <td className="px-4 py-3.5 font-mono font-medium text-slate-900">
                      REC-{proposal.id.toString().padStart(4, '0')}
                    </td>
                    <td className="px-4 py-3.5 font-medium text-slate-900">
                      {proposal.medicine_name}
                      <div className="text-[10px] text-slate-400 font-mono">Lot: {proposal.batch_number}</div>
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="flex items-center gap-1.5 text-slate-800">
                        <span className="font-medium text-slate-700">{proposal.source_facility_name}</span>
                        <ArrowRight className="w-3 h-3 text-slate-400 shrink-0" />
                        <span className="font-semibold text-blue-700">{proposal.target_facility_name}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3.5 text-right font-bold text-slate-900">
                      {(proposal.recommended_quantity ?? 0).toLocaleString()} units
                    </td>
                    <td className="px-4 py-3.5 text-right text-slate-600">
                      {(proposal.distance_km ?? 0).toFixed(1)} km
                    </td>
                    <td className="px-4 py-3.5 text-right font-bold text-emerald-600">
                      ETB {(proposal.net_value_saved_etb ?? 0).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    </td>
                    <td className="px-4 py-3.5">
                      {proposal.priority === 'High' ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-rose-100 text-rose-800 border border-rose-200">
                          High
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-100 text-blue-800 border border-blue-200">
                          {proposal.priority}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3.5">
                      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium ${
                        proposal.status === 'Approved'
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : proposal.status === 'Completed'
                          ? 'bg-blue-50 text-blue-700 border border-blue-200'
                          : 'bg-amber-50 text-amber-700 border border-amber-200'
                      }`}>
                        {proposal.status}
                      </span>
                    </td>
                  </tr>
                ))
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
              totalItems={filteredProposals.length}
              pageSize={pageSize}
            />
          </div>
        )}
      </div>
    </div>
  );
}
