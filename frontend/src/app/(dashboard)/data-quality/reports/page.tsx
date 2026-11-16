'use client';

import { useState } from 'react';
import { 
  FileText, 
  Download, 
  Calendar, 
  CheckCircle2, 
  ShieldCheck, 
  Building2, 
  BarChart3,
  Search
} from 'lucide-react';
import DemoAlert from '@/components/ui/DemoAlert';

interface QualityReportItem {
  id: string;
  reportPeriod: string;
  facility: string;
  overallDqi: number;
  completeness: number;
  consistency: number;
  plausibility: number;
  expiryValidity: number;
  status: 'Compliant' | 'Remediation Required';
  generatedDate: string;
}

const SAMPLE_REPORTS: QualityReportItem[] = [
  {
    id: 'DQR-2026-W45',
    reportPeriod: 'Nov 02 - Nov 08, 2026 (Week 45)',
    facility: 'Tikur Anbessa Specialized Hospital',
    overallDqi: 94.2,
    completeness: 98.5,
    consistency: 95.0,
    plausibility: 92.1,
    expiryValidity: 91.2,
    status: 'Compliant',
    generatedDate: '2026-11-09'
  },
  {
    id: 'DQR-2026-W45-SP',
    reportPeriod: 'Nov 02 - Nov 08, 2026 (Week 45)',
    facility: "St. Paul's Hospital Millennium Medical College",
    overallDqi: 91.8,
    completeness: 96.0,
    consistency: 91.5,
    plausibility: 89.0,
    expiryValidity: 90.7,
    status: 'Compliant',
    generatedDate: '2026-11-09'
  },
  {
    id: 'DQR-2026-W45-JU',
    reportPeriod: 'Nov 02 - Nov 08, 2026 (Week 45)',
    facility: 'Jimma University Medical Center',
    overallDqi: 86.4,
    completeness: 89.2,
    consistency: 84.0,
    plausibility: 85.5,
    expiryValidity: 87.0,
    status: 'Remediation Required',
    generatedDate: '2026-11-09'
  },
  {
    id: 'DQR-2026-W45-FH',
    reportPeriod: 'Nov 02 - Nov 08, 2026 (Week 45)',
    facility: 'Felege Hiwot Comprehensive Specialized Hospital',
    overallDqi: 88.9,
    completeness: 91.4,
    consistency: 87.8,
    plausibility: 88.0,
    expiryValidity: 88.5,
    status: 'Compliant',
    generatedDate: '2026-11-09'
  },
  {
    id: 'DQR-2026-W44-ALL',
    reportPeriod: 'Oct 26 - Nov 01, 2026 (Week 44)',
    facility: 'National Health Facility Network (Consolidated)',
    overallDqi: 92.5,
    completeness: 96.8,
    consistency: 92.4,
    plausibility: 90.1,
    expiryValidity: 90.8,
    status: 'Compliant',
    generatedDate: '2026-11-02'
  }
];

export default function DataQualityReportsPage() {
  const [reports] = useState<QualityReportItem[]>(SAMPLE_REPORTS);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredReports = reports.filter(r => 
    r.facility.toLowerCase().includes(searchQuery.toLowerCase()) ||
    r.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    r.reportPeriod.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const downloadReport = (report: QualityReportItem) => {
    const csvContent = 
      `Report ID,Period,Facility,Overall DQI,Completeness,Consistency,Plausibility,Expiry Validity,Status,Generated Date\n` +
      `"${report.id}","${report.reportPeriod}","${report.facility}",${report.overallDqi}%,${report.completeness}%,${report.consistency}%,${report.plausibility}%,${report.expiryValidity}%,${report.status},${report.generatedDate}\n`;
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${report.id}_data_quality_report.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      <DemoAlert 
        title="Periodic Data Quality Governance Archive"
        description="Weekly compliance snapshots recording 5-dimension Data Quality Index (DQI) grades, data readiness thresholds, and validation pass rates across Ethiopian public health facilities."
      />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Data Quality Reports & Archives</h1>
          <p className="text-sm text-slate-500 mt-1">
            Official periodic audit summaries documenting historical ledger accuracy and readiness for AI demand inference.
          </p>
        </div>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Historical Snapshots</span>
            <FileText className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-2">52 Weeks</div>
          <div className="text-xs text-slate-500 mt-1">Archived continuous compliance runs</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Network Mean DQI</span>
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">92.1%</div>
          <div className="text-xs text-emerald-700 mt-1">Grade A - Production Ready</div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Next Scheduled Snapshot</span>
            <Calendar className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-2">Sunday 23:59</div>
          <div className="text-xs text-blue-600 mt-1">Automated 5D validation cycle</div>
        </div>
      </div>

      {/* Search */}
      <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search report by ID, period, or facility name..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          />
        </div>
      </div>

      {/* Reports Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-50 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="px-4 py-3">Report ID</th>
                <th className="px-4 py-3">Evaluation Period</th>
                <th className="px-4 py-3">Facility</th>
                <th className="px-4 py-3 text-center">Overall DQI</th>
                <th className="px-4 py-3">5D Breakdown (Comp / Cons / Plaus / Exp)</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3 text-right">Export</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {filteredReports.map((report) => (
                <tr key={report.id} className="hover:bg-slate-50/80 transition">
                  <td className="px-4 py-3.5 font-mono font-medium text-blue-600">
                    {report.id}
                  </td>
                  <td className="px-4 py-3.5 text-slate-700">
                    {report.reportPeriod}
                  </td>
                  <td className="px-4 py-3.5 font-medium text-slate-900">
                    {report.facility}
                  </td>
                  <td className="px-4 py-3.5 text-center">
                    <span className="font-bold text-slate-900 text-sm">
                      {report.overallDqi.toFixed(1)}%
                    </span>
                  </td>
                  <td className="px-4 py-3.5 text-slate-500 font-mono text-[11px]">
                    {report.completeness}% / {report.consistency}% / {report.plausibility}% / {report.expiryValidity}%
                  </td>
                  <td className="px-4 py-3.5">
                    {report.status === 'Compliant' ? (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" /> Compliant
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-100 text-amber-800 border border-amber-200">
                        Action Needed
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-3.5 text-right">
                    <button
                      onClick={() => downloadReport(report)}
                      className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium transition text-[11px]"
                    >
                      <Download className="w-3 h-3" /> CSV
                    </button>
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
