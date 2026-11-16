'use client';

import { useState, useEffect } from 'react';
import { 
  CheckCircle2, 
  AlertTriangle, 
  AlertCircle, 
  Search, 
  Filter, 
  RefreshCw, 
  ShieldCheck,
  Check,
  FileSpreadsheet
} from 'lucide-react';
import { dataQualityApi, facilitiesApi } from '@/lib/api';
import { DataQualityIssue, Facility } from '@/types';
import DemoAlert from '@/components/ui/DemoAlert';
import Pagination from '@/components/ui/Pagination';
import EmptyState from '@/components/ui/EmptyState';

export default function DataQualityIssuesPage() {
  const [issues, setIssues] = useState<DataQualityIssue[]>([]);
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<number | 'all'>('all');
  const [selectedSeverity, setSelectedSeverity] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [resolvingId, setResolvingId] = useState<number | null>(null);
  const [resolutionNote, setResolutionNote] = useState('');
  const [activeModalIssue, setActiveModalIssue] = useState<DataQualityIssue | null>(null);

  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;

  useEffect(() => {
    loadData();
  }, [selectedFacility, selectedSeverity]);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [facs, issuesData] = await Promise.all([
        facilitiesApi.list(),
        dataQualityApi.listIssues(
          selectedFacility === 'all' ? undefined : selectedFacility,
          selectedSeverity === 'all' ? undefined : selectedSeverity
        ),
      ]);
      setFacilities(facs);
      setIssues(issuesData);
    } catch {
      // Fallback handled in API client
    } finally {
      setIsLoading(false);
    }
  };

  const handleResolve = async (issueId: number) => {
    try {
      await dataQualityApi.resolveIssue(issueId, resolutionNote || 'Resolved by user triage');
      setIssues(prev => prev.map(iss => iss.id === issueId ? { ...iss, is_resolved: true } : iss));
      setActiveModalIssue(null);
      setResolutionNote('');
    } catch {
      // Optimistic update
      setIssues(prev => prev.map(iss => iss.id === issueId ? { ...iss, is_resolved: true } : iss));
      setActiveModalIssue(null);
    }
  };

  const filteredIssues = issues.filter(issue => {
    const term = searchQuery.toLowerCase();
    const facilityMatch = (issue.facility_name ?? '').toLowerCase().includes(term);
    const medicineMatch = (issue.medicine_name ?? '').toLowerCase().includes(term);
    const descMatch = (issue.description ?? '').toLowerCase().includes(term);
    const typeMatch = (issue.issue_type ?? '').toLowerCase().includes(term);
    return facilityMatch || medicineMatch || descMatch || typeMatch;
  });

  const totalPages = Math.ceil(filteredIssues.length / pageSize) || 1;
  const paginatedIssues = filteredIssues.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  const criticalCount = issues.filter(i => i.severity === 'CRITICAL' && !i.is_resolved).length;
  const warningCount = issues.filter(i => i.severity === 'WARNING' && !i.is_resolved).length;
  const resolvedCount = issues.filter(i => i.is_resolved).length;

  return (
    <div className="space-y-6">
      <DemoAlert 
        title="Automated Data Quality Audit Queue"
        description="Continuous 5-dimension validation engine detecting missing timestamps, duplicate SKUs, inverted expiry sequences, and volume discrepancies across facility ledgers."
      />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Data Quality Issues Queue</h1>
          <p className="text-sm text-slate-500 mt-1">
            Triaged remediation ledger for electronic stock ledger anomalies prior to AI inference ingestion.
          </p>
        </div>
        <button
          onClick={loadData}
          disabled={isLoading}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-300 bg-white text-xs font-medium text-slate-700 hover:bg-slate-50 shadow-sm transition"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-slate-500 ${isLoading ? 'animate-spin' : ''}`} />
          Refresh Queue
        </button>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Critical Validation Failures</span>
            <AlertCircle className="w-4 h-4 text-rose-600" />
          </div>
          <div className="text-2xl font-bold text-rose-600 mt-2">{criticalCount}</div>
          <div className="text-xs text-rose-700 mt-1">Blocks automated redistribution generation</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Warning Level Anomalies</span>
            <AlertTriangle className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-amber-600 mt-2">{warningCount}</div>
          <div className="text-xs text-amber-700 mt-1">Plausibility or near-threshold warnings</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Remediated & Verified</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-2">{resolvedCount}</div>
          <div className="text-xs text-emerald-600 mt-1">Cleared by facility pharmacists</div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search by medicine, facility, issue type, or description..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
          </input>
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
            value={selectedSeverity}
            onChange={(e) => setSelectedSeverity(e.target.value)}
            className="text-xs border border-slate-300 rounded-lg px-2.5 py-1.5 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="WARNING">Warning</option>
            <option value="INFO">Informational</option>
          </select>
        </div>
      </div>

      {/* Issues Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-50 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="px-4 py-3">Severity</th>
                <th className="px-4 py-3">Issue Type</th>
                <th className="px-4 py-3">Facility</th>
                <th className="px-4 py-3">Medicine / Field</th>
                <th className="px-4 py-3">Description</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {paginatedIssues.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-12 text-center text-slate-500">
                    <EmptyState
                      title="No Data Quality Issues Found"
                      description="All records meet integrity requirements or match current filter parameters."
                    />
                  </td>
                </tr>
              ) : (
                paginatedIssues.map((issue) => (
                  <tr key={issue.id} className="hover:bg-slate-50/80 transition">
                    <td className="px-4 py-3">
                      {issue.severity === 'CRITICAL' ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-semibold bg-rose-100 text-rose-800 border border-rose-200">
                          <AlertCircle className="w-3 h-3 text-rose-600" /> CRITICAL
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-100 text-amber-800 border border-amber-200">
                          <AlertTriangle className="w-3 h-3 text-amber-600" /> WARNING
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3 font-medium text-slate-900">
                      {issue.issue_type}
                    </td>
                    <td className="px-4 py-3 text-slate-700">
                      {issue.facility_name ?? `Facility #${issue.facility_id}`}
                    </td>
                    <td className="px-4 py-3">
                      <div className="font-medium text-slate-800">{issue.medicine_name ?? 'Catalog-wide'}</div>
                      {issue.field_name && (
                        <div className="text-[10px] text-slate-400 font-mono">Field: {issue.field_name}</div>
                      )}
                    </td>
                    <td className="px-4 py-3 max-w-xs text-slate-600">
                      {issue.description}
                    </td>
                    <td className="px-4 py-3">
                      {issue.is_resolved ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                          <Check className="w-3 h-3" /> Resolved
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-600">
                          Pending
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-right">
                      {!issue.is_resolved && (
                        <button
                          onClick={() => setActiveModalIssue(issue)}
                          className="px-2.5 py-1 rounded bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200 font-medium transition text-[11px]"
                        >
                          Resolve
                        </button>
                      )}
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
              totalItems={filteredIssues.length}
              pageSize={pageSize}
            />
          </div>
        )}
      </div>

      {/* Resolution Modal */}
      {activeModalIssue && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl border border-slate-200 shadow-xl max-w-md w-full p-6 space-y-4">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-blue-600" />
              <h3 className="text-base font-semibold text-slate-900">Resolve Data Quality Anomaly</h3>
            </div>
            
            <div className="text-xs text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-200 space-y-1">
              <div><strong className="text-slate-800">Issue:</strong> {activeModalIssue.issue_type}</div>
              <div><strong className="text-slate-800">Facility:</strong> {activeModalIssue.facility_name}</div>
              <div><strong className="text-slate-800">Details:</strong> {activeModalIssue.description}</div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Remediation Note</label>
              <textarea
                rows={3}
                value={resolutionNote}
                onChange={(e) => setResolutionNote(e.target.value)}
                placeholder="Describe corrective action taken (e.g., corrected batch lot number in ledger, stock count reconciled)..."
                className="w-full text-xs border border-slate-300 rounded-lg p-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
              />
            </div>

            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setActiveModalIssue(null)}
                className="px-3 py-1.5 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-50 text-xs font-medium"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => handleResolve(activeModalIssue.id)}
                className="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium shadow-xs"
              >
                Confirm Resolution
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
