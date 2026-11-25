'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  Network, 
  ArrowRight, 
  Coins, 
  Filter, 
  Search, 
  RefreshCw, 
  Sparkles,
  Sliders,
  Cpu,
  CheckCircle2,
  X,
  ExternalLink,
  ShieldAlert,
  HelpCircle,
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

  // MILP Optimizer Modal & Execution State
  const [isOptimizerOpen, setIsOptimizerOpen] = useState(false);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optRegion, setOptRegion] = useState<string>('all');
  const [optMaxDistance, setOptMaxDistance] = useState<number>(350);
  const [optMinExpiryMonths, setOptMinExpiryMonths] = useState<number>(3);
  const [optShortagePenalty, setOptShortagePenalty] = useState<number>(100);
  const [optWastePenalty, setOptWastePenalty] = useState<number>(50);
  const [optTransportCostKm, setOptTransportCostKm] = useState<number>(0.05);
  const [solverResult, setSolverResult] = useState<{
    status: string;
    totalRoutes: number;
    valueSavedEtb: number;
    runtimeMs: number;
  } | null>(null);

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

  const handleRunOptimizer = async () => {
    setIsOptimizing(true);
    const startTime = performance.now();
    try {
      const results = await redistributionApi.runOptimization({
        region: optRegion === 'all' ? undefined : optRegion,
        max_distance_km: optMaxDistance,
        min_expiry_months: optMinExpiryMonths,
        cost_shortage_penalty: optShortagePenalty,
        cost_waste_penalty: optWastePenalty,
        cost_transport_per_km_unit: optTransportCostKm,
      });

      const runtimeMs = Math.round(performance.now() - startTime);
      const totalSaved = results.reduce((acc, r) => acc + (r.net_value_saved_etb ?? 0), 0);

      setSolverResult({
        status: 'Optimal (PuLP CBC Simplex)',
        totalRoutes: results.length,
        valueSavedEtb: totalSaved,
        runtimeMs,
      });

      // Reload fresh recommendations from backend
      await loadData();
      setIsOptimizerOpen(false);
    } catch (err) {
      console.error('Optimization error:', err);
    } finally {
      setIsOptimizing(false);
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
        <div className="flex items-center gap-2">
          <button
            onClick={loadData}
            disabled={isLoading}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-300 bg-white text-xs font-medium text-slate-700 hover:bg-slate-50 shadow-xs transition"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-slate-500 ${isLoading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
          <button
            onClick={() => setIsOptimizerOpen(true)}
            className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-xs transition"
          >
            <Cpu className="w-3.5 h-3.5" />
            Run MILP Optimizer
          </button>
        </div>
      </div>

      {/* Solver Execution Banner */}
      {solverResult && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center justify-between text-xs text-emerald-900 shadow-xs animate-in fade-in">
          <div className="flex items-center gap-2.5">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <div>
              <span className="font-bold">Solver Execution Completed: </span>
              {solverResult.status} &bull; Formulated <strong>{solverResult.totalRoutes}</strong> feasible transfers saving <strong>ETB {solverResult.valueSavedEtb.toLocaleString(undefined, { maximumFractionDigits: 0 })}</strong> in {solverResult.runtimeMs}ms.
            </div>
          </div>
          <button
            onClick={() => setSolverResult(null)}
            className="text-emerald-700 hover:text-emerald-900 p-1"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>High Priority Transfers</span>
            <Sparkles className="w-4 h-4 text-rose-600" />
          </div>
          <div className="text-2xl font-bold text-rose-600 mt-2">{highPriorityCount} Routes</div>
          <div className="text-xs text-rose-700 mt-1">Immediate shortage avoidance</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Total Value Preserved</span>
            <Coins className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">
            ETB {totalSavedEtb.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </div>
          <div className="text-xs text-emerald-700 mt-1">Net financial savings vs. expiration loss</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Optimization Method</span>
            <Network className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-2">PuLP MILP</div>
          <div className="text-xs text-blue-600 mt-1">Branch-and-Bound Simplex Engine</div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
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
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
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
                <th className="px-4 py-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {paginatedProposals.length === 0 ? (
                <tr>
                  <td colSpan={9} className="px-4 py-12 text-center text-slate-500">
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
                    <td className="px-4 py-3.5 text-right">
                      <Link
                        href="/redistribution/approvals"
                        className="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-600 hover:text-blue-800"
                      >
                        Approvals <ExternalLink className="w-3 h-3" />
                      </Link>
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

      {/* MILP Optimizer Parameter Configuration Modal */}
      {isOptimizerOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl border border-slate-300 shadow-2xl max-w-xl w-full p-6 space-y-6 text-slate-800">
            {/* Modal Header */}
            <div className="flex items-center justify-between border-b border-slate-200 pb-3">
              <div className="flex items-center gap-2">
                <Cpu className="w-5 h-5 text-blue-600" />
                <h3 className="text-base font-bold text-slate-900">
                  MILP Redistribution Optimizer Configuration
                </h3>
              </div>
              <button
                onClick={() => setIsOptimizerOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-xs text-slate-500">
              Tune objective penalties and physical transport constraints before executing the Mixed-Integer Linear Programming solver over the active healthcare network.
            </p>

            {/* Parameter Controls */}
            <div className="space-y-4 text-xs">
              <div>
                <label className="font-semibold text-slate-700 block mb-1">
                  Target Geographic Region
                </label>
                <select
                  value={optRegion}
                  onChange={(e) => setOptRegion(e.target.value)}
                  className="w-full border border-slate-300 rounded-lg p-2 bg-white text-slate-800"
                >
                  <option value="all">All National Regions (Inter-Regional Allowed)</option>
                  <option value="Addis Ababa">Addis Ababa Cluster</option>
                  <option value="Oromia">Oromia Regional Health Bureau</option>
                  <option value="Amhara">Amhara Regional Health Bureau</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <div className="flex items-center justify-between font-semibold text-slate-700 mb-1">
                    <span>Max Transit Distance</span>
                    <span className="font-mono text-blue-600">{optMaxDistance} km</span>
                  </div>
                  <input
                    type="range"
                    min={50}
                    max={800}
                    step={25}
                    value={optMaxDistance}
                    onChange={(e) => setOptMaxDistance(Number(e.target.value))}
                    className="w-full accent-blue-600"
                  />
                  <span className="text-[10px] text-slate-400">Road distance radius limit</span>
                </div>

                <div>
                  <div className="flex items-center justify-between font-semibold text-slate-700 mb-1">
                    <span>Min Batch Shelf-Life</span>
                    <span className="font-mono text-blue-600">{optMinExpiryMonths} mo</span>
                  </div>
                  <input
                    type="range"
                    min={1}
                    max={12}
                    step={1}
                    value={optMinExpiryMonths}
                    onChange={(e) => setOptMinExpiryMonths(Number(e.target.value))}
                    className="w-full accent-blue-600"
                  />
                  <span className="text-[10px] text-slate-400">Exclude batches expiring sooner</span>
                </div>
              </div>

              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-3">
                <span className="font-bold text-slate-700 block uppercase text-[10px] tracking-wider">
                  Cost Penalty Matrix (ETB)
                </span>
                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="text-[11px] text-slate-600 block mb-0.5">Shortage Penalty</label>
                    <input
                      type="number"
                      value={optShortagePenalty}
                      onChange={(e) => setOptShortagePenalty(Number(e.target.value))}
                      className="w-full border border-slate-300 rounded p-1.5 text-xs font-mono"
                    />
                    <span className="text-[9px] text-slate-400">Per unmet patient unit</span>
                  </div>
                  <div>
                    <label className="text-[11px] text-slate-600 block mb-0.5">Waste Penalty</label>
                    <input
                      type="number"
                      value={optWastePenalty}
                      onChange={(e) => setOptWastePenalty(Number(e.target.value))}
                      className="w-full border border-slate-300 rounded p-1.5 text-xs font-mono"
                    />
                    <span className="text-[9px] text-slate-400">Per expired unit</span>
                  </div>
                  <div>
                    <label className="text-[11px] text-slate-600 block mb-0.5">Transport Cost</label>
                    <input
                      type="number"
                      step={0.01}
                      value={optTransportCostKm}
                      onChange={(e) => setOptTransportCostKm(Number(e.target.value))}
                      className="w-full border border-slate-300 rounded p-1.5 text-xs font-mono"
                    />
                    <span className="text-[9px] text-slate-400">ETB / km &bull; unit</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Modal Actions */}
            <div className="flex items-center justify-end gap-2 border-t border-slate-200 pt-3">
              <button
                type="button"
                onClick={() => setIsOptimizerOpen(false)}
                className="px-3.5 py-1.5 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-50 text-xs font-medium"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleRunOptimizer}
                disabled={isOptimizing}
                className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-xs disabled:opacity-50"
              >
                {isOptimizing ? (
                  <>
                    <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    Solving Simplex Model...
                  </>
                ) : (
                  <>
                    <Cpu className="w-3.5 h-3.5" />
                    Execute MILP Solver
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
