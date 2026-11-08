'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { batchesApi, facilitiesApi } from '@/lib/api';
import { BatchItem, Facility } from '@/types';
import { Search, CalendarClock, Clock, AlertTriangle, ShieldCheck } from 'lucide-react';
import Link from 'next/link';

export default function BatchesPage() {
  const [batches, setBatches] = useState<BatchItem[]>([]);
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<number | undefined>(undefined);
  const [selectedStatus, setSelectedStatus] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [facs, bList] = await Promise.all([
          facilitiesApi.list(),
          batchesApi.list(selectedFacility, undefined, selectedStatus === 'All' ? undefined : selectedStatus),
        ]);
        setFacilities(facs);
        setBatches(bList);
      } catch (err) {
        console.error('Failed to load batches:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, [selectedFacility, selectedStatus]);

  const filteredBatches = batches.filter((b) => {
    const q = searchQuery.toLowerCase();
    const batchMatch = b.batch_number.toLowerCase().includes(q);
    const medMatch = b.medicine_name?.toLowerCase().includes(q) || false;
    return batchMatch || medMatch;
  });

  const getExpiryBadge = (days?: number) => {
    if (days === undefined) return null;
    if (days <= 30) {
      return <Badge variant="danger">{days}d Critical Expiry</Badge>;
    }
    if (days <= 90) {
      return <Badge variant="warning">{days}d Warning (&lt;90d)</Badge>;
    }
    return <Badge variant="success">{days}d Shelf Life</Badge>;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-slate-200/80 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Pharmaceutical Batch & Lot Tracking
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Traceability of lot numbers, manufacturing and expiration dates under FEFO (First-Expired, First-Out).
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search lot number or medicine..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <select
            value={selectedFacility || ''}
            onChange={(e) => setSelectedFacility(e.target.value ? Number(e.target.value) : undefined)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="">All Facilities</option>
            {facilities.map((f) => (
              <option key={f.id} value={f.id}>
                {f.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="All">All Lot Statuses</option>
            <option value="Active">Active</option>
            <option value="Quarantined">Quarantined</option>
            <option value="Expired">Expired</option>
          </select>
        </div>
      </div>

      {/* Batches Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
              <tr>
                <th className="px-6 py-3.5">Batch / Lot Number</th>
                <th className="px-6 py-3.5">Medicine</th>
                <th className="px-6 py-3.5">Facility</th>
                <th className="px-6 py-3.5">Expiry Date</th>
                <th className="px-6 py-3.5">Remaining Stock</th>
                <th className="px-6 py-3.5">Unit Cost (ETB)</th>
                <th className="px-6 py-3.5">Shelf Life Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredBatches.map((b) => (
                <tr key={b.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="px-6 py-3.5 font-mono font-semibold text-slate-900">
                    {b.batch_number}
                  </td>
                  <td className="px-6 py-3.5 font-medium text-slate-800">
                    {b.medicine_name}
                  </td>
                  <td className="px-6 py-3.5 text-slate-600">
                    {b.facility_name || 'Tikur Anbessa Hospital'}
                  </td>
                  <td className="px-6 py-3.5 font-mono text-slate-700">
                    {b.expiry_date}
                  </td>
                  <td className="px-6 py-3.5 font-semibold text-slate-900">
                    {b.current_quantity.toLocaleString()} units
                  </td>
                  <td className="px-6 py-3.5 font-medium text-slate-800">
                    {b.unit_cost.toFixed(2)} ETB
                  </td>
                  <td className="px-6 py-3.5">
                    {getExpiryBadge(b.days_to_expiry)}
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
