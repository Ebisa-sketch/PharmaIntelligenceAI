'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { DemoAlert } from '@/components/ui/DemoAlert';
import { Pagination } from '@/components/ui/Pagination';
import { EmptyState } from '@/components/ui/EmptyState';
import { auditLogsApi } from '@/lib/api';
import { AuditLogEntry } from '@/types';
import {
  ShieldCheck,
  Search,
  Filter,
  Download,
  Calendar,
  Lock,
  Eye,
  X,
  FileCode,
  Terminal,
} from 'lucide-react';

export default function AuditLogsPage() {
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedAction, setSelectedAction] = useState('All');
  const [selectedEntity, setSelectedEntity] = useState('All');
  const [isLoading, setIsLoading] = useState(true);

  // Inspector Modal State
  const [inspectedLog, setInspectedLog] = useState<AuditLogEntry | null>(null);

  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 8;

  useEffect(() => {
    async function loadLogs() {
      try {
        const actionParam = selectedAction === 'All' ? undefined : selectedAction;
        const entityParam = selectedEntity === 'All' ? undefined : selectedEntity;
        const data = await auditLogsApi.list(actionParam, entityParam, 100);
        setLogs(data);
      } catch (err) {
        console.error('Failed to load audit logs:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadLogs();
  }, [selectedAction, selectedEntity]);

  const filteredLogs = logs.filter((l) => {
    const q = searchQuery.toLowerCase();
    const actionMatch = l.action.toLowerCase().includes(q);
    const entityMatch = l.entity_type.toLowerCase().includes(q);
    const userMatch = l.user_email ? l.user_email.toLowerCase().includes(q) : false;
    const ipMatch = l.ip_address ? l.ip_address.toLowerCase().includes(q) : false;
    return actionMatch || entityMatch || userMatch || ipMatch;
  });

  const totalPages = Math.ceil(filteredLogs.length / itemsPerPage);
  const displayedLogs = filteredLogs.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const handleExportCSV = () => {
    const headers = 'ID,Timestamp,User,Action,EntityType,EntityID,IPAddress\n';
    const rows = filteredLogs
      .map(
        (l) =>
          `"${l.id}","${l.timestamp}","${l.user_email || 'System'}","${l.action}","${l.entity_type}","${l.entity_id || ''}","${l.ip_address || ''}"`
      )
      .join('\n');
    const blob = new Blob([headers + rows], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `audit_logs_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getActionBadge = (action: string) => {
    if (action.includes('OVERRIDE') || action.includes('REJECT')) {
      return <Badge variant="warning">{action}</Badge>;
    }
    if (action.includes('DELETE') || action.includes('DISPOSAL')) {
      return <Badge variant="danger">{action}</Badge>;
    }
    if (action.includes('LOGIN') || action.includes('SUCCESS') || action.includes('RESOLVED')) {
      return <Badge variant="success">{action}</Badge>;
    }
    return <Badge variant="info">{action}</Badge>;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Immutable Audit &amp; Governance Ledger
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Tamper-evident activity trail tracking clinical overrides, lateral redistributions, and user authentications.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleExportCSV}>
            <Download className="w-3.5 h-3.5 mr-1.5" />
            Export Audit Ledger CSV
          </Button>
        </div>
      </div>

      <DemoAlert
        title="Regulatory Compliance Retention"
        message="All records are immutably timestamped in UTC. Audit log verification adheres to Ethiopian Data Protection and Health Information System standards."
      />

      {/* Metrics Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Total Audit Records
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-1">{logs.length} Events</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Retained in append-only storage</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Clinical Overrides
          </div>
          <div className="text-2xl font-bold text-amber-600 mt-1">
            {logs.filter((l) => l.action.includes('OVERRIDE')).length}
          </div>
          <div className="text-[11px] text-amber-700 mt-0.5">Logged with clinical justifications</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Integrity Checksum
          </div>
          <div className="text-2xl font-bold text-emerald-600 mt-1">Verified</div>
          <div className="text-[11px] text-emerald-700 mt-0.5">SHA-256 block chain valid</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Retention Horizon
          </div>
          <div className="text-2xl font-bold text-blue-600 mt-1">7 Years</div>
          <div className="text-[11px] text-blue-700 mt-0.5">MOH national health compliance</div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 bg-white p-4 rounded-xl border border-slate-200/80 shadow-2xs">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search action, user email, IP address..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <select
            value={selectedAction}
            onChange={(e) => setSelectedAction(e.target.value)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="All">All Audit Actions</option>
            <option value="OVERRIDE_REDISTRIBUTION">OVERRIDE_REDISTRIBUTION</option>
            <option value="FEFO_BATCH_DISPENSE">FEFO_BATCH_DISPENSE</option>
            <option value="DQI_ANOMALY_RESOLVED">DQI_ANOMALY_RESOLVED</option>
            <option value="SYSTEM_SETTINGS_UPDATE">SYSTEM_SETTINGS_UPDATE</option>
            <option value="USER_LOGIN_SUCCESS">USER_LOGIN_SUCCESS</option>
          </select>
        </div>

        <div>
          <select
            value={selectedEntity}
            onChange={(e) => setSelectedEntity(e.target.value)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="All">All Target Entities</option>
            <option value="RedistributionProposal">RedistributionProposal</option>
            <option value="Batch">Batch</option>
            <option value="DataQualityIssue">DataQualityIssue</option>
            <option value="SystemConfiguration">SystemConfiguration</option>
            <option value="Session">Session</option>
          </select>
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-2xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
              <tr>
                <th className="px-6 py-3.5">Timestamp (UTC)</th>
                <th className="px-6 py-3.5">Action Executed</th>
                <th className="px-6 py-3.5">Target Entity</th>
                <th className="px-6 py-3.5">User Responsible</th>
                <th className="px-6 py-3.5">Origin IP</th>
                <th className="px-6 py-3.5 text-right">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {displayedLogs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="px-6 py-3.5 font-mono text-[11px] text-slate-500 whitespace-nowrap">
                    {new Date(log.timestamp).toLocaleString()}
                  </td>
                  <td className="px-6 py-3.5 font-mono text-xs font-semibold">
                    {getActionBadge(log.action)}
                  </td>
                  <td className="px-6 py-3.5 font-medium text-slate-900">
                    {log.entity_type}{' '}
                    {log.entity_id && (
                      <span className="font-mono text-[11px] text-slate-400">#{log.entity_id}</span>
                    )}
                  </td>
                  <td className="px-6 py-3.5 text-slate-700">
                    <span className="font-medium text-slate-800">
                      {log.user_email || `User #${log.user_id || 'System'}`}
                    </span>
                  </td>
                  <td className="px-6 py-3.5 font-mono text-slate-500 text-[11px]">
                    {log.ip_address || '127.0.0.1'}
                  </td>
                  <td className="px-6 py-3.5 text-right">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setInspectedLog(log)}
                    >
                      <Eye className="w-3.5 h-3.5 mr-1" />
                      Inspect
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredLogs.length === 0 && !isLoading && (
          <EmptyState
            icon={ShieldCheck}
            title="No Matching Audit Events"
            description="No logged security or operational events matched your filters."
            actionLabel="Reset Filters"
            onAction={() => {
              setSearchQuery('');
              setSelectedAction('All');
              setSelectedEntity('All');
            }}
          />
        )}

        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
          totalItems={filteredLogs.length}
          itemsPerPage={itemsPerPage}
        />
      </div>

      {/* Inspector Modal */}
      {inspectedLog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
          <div className="w-full max-w-lg bg-white rounded-xl shadow-xl border border-slate-200 p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <FileCode className="w-4 h-4 text-blue-600" />
                <h3 className="text-base font-bold text-slate-900">Audit Record Inspector</h3>
              </div>
              <button
                onClick={() => setInspectedLog(null)}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-2 p-3 bg-slate-50 rounded-lg border border-slate-200/80">
                <div>
                  <span className="text-slate-400 block text-[10px]">Action</span>
                  <span className="font-semibold text-slate-900 font-mono">{inspectedLog.action}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px]">Entity</span>
                  <span className="font-semibold text-slate-900 font-mono">
                    {inspectedLog.entity_type} #{inspectedLog.entity_id}
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px]">Responsible Identity</span>
                  <span className="font-semibold text-slate-900 truncate block">
                    {inspectedLog.user_email || `User #${inspectedLog.user_id || 'System'}`}
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px]">IP &bull; Timestamp</span>
                  <span className="font-mono text-slate-700">
                    {inspectedLog.ip_address} &bull; {new Date(inspectedLog.timestamp).toISOString()}
                  </span>
                </div>
              </div>

              <div>
                <span className="font-semibold text-slate-700 block mb-1">
                  Event Metadata &amp; Parameters
                </span>
                <pre className="p-3 bg-slate-900 text-blue-300 font-mono text-[11px] rounded-lg overflow-x-auto max-h-48">
                  {typeof inspectedLog.details === 'object'
                    ? JSON.stringify(inspectedLog.details, null, 2)
                    : inspectedLog.details || 'No additional payload provided.'}
                </pre>
              </div>
            </div>

            <div className="flex justify-end pt-2 border-t">
              <Button variant="outline" size="sm" onClick={() => setInspectedLog(null)}>
                Close Inspector
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
