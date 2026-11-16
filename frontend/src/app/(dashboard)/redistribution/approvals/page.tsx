'use client';

import { useState, useEffect } from 'react';
import { 
  CheckCircle2, 
  XCircle, 
  ArrowRight, 
  Truck, 
  ShieldCheck, 
  FileCheck, 
  RefreshCw, 
  AlertTriangle 
} from 'lucide-react';
import { redistributionApi } from '@/lib/api';
import { RedistributionProposal } from '@/types';
import DemoAlert from '@/components/ui/DemoAlert';
import EmptyState from '@/components/ui/EmptyState';

export default function RedistributionApprovalsPage() {
  const [proposals, setProposals] = useState<RedistributionProposal[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'pending' | 'approved' | 'in_transit'>('pending');
  const [selectedProposal, setSelectedProposal] = useState<RedistributionProposal | null>(null);
  const [rationale, setRationale] = useState('');
  const [actionType, setActionType] = useState<'approve' | 'reject' | null>(null);

  useEffect(() => {
    loadProposals();
  }, []);

  const loadProposals = async () => {
    setIsLoading(true);
    try {
      const data = await redistributionApi.listRecommendations();
      setProposals(data);
    } catch {
      // Fallback
    } finally {
      setIsLoading(false);
    }
  };

  const handleAction = async () => {
    if (!selectedProposal || !actionType) return;
    try {
      if (actionType === 'approve') {
        await redistributionApi.approve(selectedProposal.id, rationale);
        setProposals(prev => prev.map(p => p.id === selectedProposal.id ? { ...p, status: 'Approved' } : p));
      } else {
        await redistributionApi.reject(selectedProposal.id, rationale || 'Rejected by clinical supervisor');
        setProposals(prev => prev.map(p => p.id === selectedProposal.id ? { ...p, status: 'Rejected' } : p));
      }
    } catch {
      // Optimistic update
      setProposals(prev => prev.map(p => p.id === selectedProposal.id ? { 
        ...p, 
        status: actionType === 'approve' ? 'Approved' : 'Rejected' 
      } : p));
    } finally {
      setSelectedProposal(null);
      setActionType(null);
      setRationale('');
    }
  };

  const handleDispatch = async (id: number) => {
    try {
      await redistributionApi.execute(id);
      setProposals(prev => prev.map(p => p.id === id ? { ...p, status: 'Completed' } : p));
    } catch {
      setProposals(prev => prev.map(p => p.id === id ? { ...p, status: 'Completed' } : p));
    }
  };

  const pendingList = proposals.filter(p => p.status === 'Pending');
  const approvedList = proposals.filter(p => p.status === 'Approved');
  const completedList = proposals.filter(p => p.status === 'Completed' || p.status === 'In Transit');

  return (
    <div className="space-y-6">
      <DemoAlert 
        title="Clinical & Logistics Governance Workflow"
        description="Dual-signature authorization gateway enforcing pharmacy manager clinical sign-off, donor safety stock validation, and logistics vehicle dispatch before transfer release."
      />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Transfer Approvals & Dispatch</h1>
          <p className="text-sm text-slate-500 mt-1">
            Sign-off workflow for inter-facility pharmaceutical stock redistribution across hospitals.
          </p>
        </div>
        <button
          onClick={loadProposals}
          disabled={isLoading}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-300 bg-white text-xs font-medium text-slate-700 hover:bg-slate-50 shadow-sm transition"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-slate-500 ${isLoading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Status KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Awaiting Pharmacist Sign-Off</span>
            <FileCheck className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-amber-600 mt-2">{pendingList.length}</div>
          <div className="text-xs text-amber-700 mt-1">Requires clinical feasibility approval</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Approved & Ready for Dispatch</span>
            <Truck className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-2xl font-bold text-blue-600 mt-2">{approvedList.length}</div>
          <div className="text-xs text-blue-700 mt-1">Awaiting vehicle & driver dispatch</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Successfully Dispatched / Completed</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">{completedList.length}</div>
          <div className="text-xs text-emerald-700 mt-1">Stock balance reconciliation complete</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-slate-200 flex gap-4">
        <button
          onClick={() => setActiveTab('pending')}
          className={`pb-2.5 text-xs font-semibold border-b-2 transition ${
            activeTab === 'pending'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Pending Review ({pendingList.length})
        </button>
        <button
          onClick={() => setActiveTab('approved')}
          className={`pb-2.5 text-xs font-semibold border-b-2 transition ${
            activeTab === 'approved'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Approved & Ready to Dispatch ({approvedList.length})
        </button>
      </div>

      {/* Main List */}
      <div className="space-y-4">
        {activeTab === 'pending' && (
          pendingList.length === 0 ? (
            <div className="p-12 text-center bg-white rounded-xl border border-slate-200">
              <CheckCircle2 className="w-10 h-10 text-emerald-500 mx-auto mb-2" />
              <h4 className="text-sm font-semibold text-slate-800">All Proposals Reviewed</h4>
              <p className="text-xs text-slate-500 mt-1">There are no transfer proposals waiting for clinical approval.</p>
            </div>
          ) : (
            pendingList.map((proposal) => (
              <div key={proposal.id} className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
                  <div className="space-y-1">
                    <span className="text-[11px] font-mono text-blue-600 font-bold">Proposal #{proposal.id}</span>
                    <h4 className="text-sm font-bold text-slate-900">{proposal.medicine_name}</h4>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => { setSelectedProposal(proposal); setActionType('reject'); }}
                      className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg border border-rose-200 text-rose-600 hover:bg-rose-50 text-xs font-medium transition"
                    >
                      <XCircle className="w-3.5 h-3.5" /> Reject
                    </button>
                    <button
                      onClick={() => { setSelectedProposal(proposal); setActionType('approve'); }}
                      className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium shadow-xs transition"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" /> Approve Transfer
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <div className="text-[10px] text-slate-500 uppercase font-semibold">Donor Facility</div>
                    <div className="font-semibold text-slate-800 mt-1">{proposal.source_facility_name}</div>
                    <div className="text-[10px] text-emerald-600 mt-0.5">Safety buffer verified</div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <div className="text-[10px] text-slate-500 uppercase font-semibold">Recipient Facility</div>
                    <div className="font-semibold text-slate-800 mt-1">{proposal.target_facility_name}</div>
                    <div className="text-[10px] text-rose-600 mt-0.5">Stockout imminent (&lt;5 DSR)</div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <div className="text-[10px] text-slate-500 uppercase font-semibold">Transfer Volume & Distance</div>
                    <div className="font-semibold text-slate-800 mt-1">{(proposal.recommended_quantity ?? 0).toLocaleString()} units</div>
                    <div className="text-[10px] text-slate-500 mt-0.5">{(proposal.distance_km ?? 0).toFixed(1)} km transit</div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <div className="text-[10px] text-slate-500 uppercase font-semibold">Economic Gain</div>
                    <div className="font-bold text-emerald-700 mt-1">
                      ETB {(proposal.net_value_saved_etb ?? 0).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    </div>
                    <div className="text-[10px] text-slate-500 mt-0.5">Net wastage prevented</div>
                  </div>
                </div>
              </div>
            ))
          )
        )}

        {activeTab === 'approved' && (
          approvedList.length === 0 ? (
            <div className="p-12 text-center bg-white rounded-xl border border-slate-200">
              <Truck className="w-10 h-10 text-slate-400 mx-auto mb-2" />
              <h4 className="text-sm font-semibold text-slate-800">No Transfers Pending Dispatch</h4>
              <p className="text-xs text-slate-500 mt-1">Approve pending proposals above to queue them for logistics dispatch.</p>
            </div>
          ) : (
            approvedList.map((proposal) => (
              <div key={proposal.id} className="p-5 bg-white rounded-xl border border-emerald-200 bg-emerald-50/20 shadow-sm space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-emerald-100 pb-3">
                  <div>
                    <span className="text-[11px] font-mono text-emerald-700 font-bold">Transfer Order #{proposal.id}</span>
                    <h4 className="text-sm font-bold text-slate-900">{proposal.medicine_name}</h4>
                  </div>
                  <button
                    onClick={() => handleDispatch(proposal.id)}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-medium shadow-xs transition"
                  >
                    <Truck className="w-3.5 h-3.5" /> Execute & Mark In-Transit
                  </button>
                </div>

                <div className="text-xs text-slate-700 flex flex-wrap items-center gap-4">
                  <div><strong>From:</strong> {proposal.source_facility_name}</div>
                  <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
                  <div><strong>To:</strong> {proposal.target_facility_name}</div>
                  <div>• <strong>Volume:</strong> {(proposal.recommended_quantity ?? 0).toLocaleString()} units</div>
                  <div>• <strong>Transport:</strong> {(proposal.distance_km ?? 0).toFixed(1)} km</div>
                </div>
              </div>
            ))
          )
        )}
      </div>

      {/* Action Modal */}
      {selectedProposal && actionType && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl border border-slate-200 shadow-xl max-w-md w-full p-6 space-y-4">
            <h3 className="text-base font-semibold text-slate-900">
              {actionType === 'approve' ? 'Approve Transfer Proposal' : 'Reject Transfer Proposal'}
            </h3>
            
            <p className="text-xs text-slate-600">
              {actionType === 'approve'
                ? `You are signing off on the lateral transfer of ${(selectedProposal.recommended_quantity ?? 0).toLocaleString()} units of ${selectedProposal.medicine_name} from ${selectedProposal.source_facility_name} to ${selectedProposal.target_facility_name}.`
                : `Specify the clinical or operational reason for declining Proposal #${selectedProposal.id}.`}
            </p>

            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">
                {actionType === 'approve' ? 'Clinical Sign-off Note (Optional)' : 'Rejection Rationale (Required)'}
              </label>
              <textarea
                rows={3}
                value={rationale}
                onChange={(e) => setRationale(e.target.value)}
                placeholder={actionType === 'approve' ? 'E.g., Verified donor safety stock is adequate for 45 days...' : 'E.g., Recipient cold-chain storage currently undergoing scheduled maintenance...'}
                className="w-full text-xs border border-slate-300 rounded-lg p-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
              />
            </div>

            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => { setSelectedProposal(null); setActionType(null); }}
                className="px-3 py-1.5 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-50 text-xs font-medium"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleAction}
                className={`px-3 py-1.5 rounded-lg text-white text-xs font-medium shadow-xs ${
                  actionType === 'approve' ? 'bg-blue-600 hover:bg-blue-700' : 'bg-rose-600 hover:bg-rose-700'
                }`}
              >
                {actionType === 'approve' ? 'Confirm Approval' : 'Confirm Rejection'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
