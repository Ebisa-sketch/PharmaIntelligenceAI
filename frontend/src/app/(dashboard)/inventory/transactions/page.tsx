'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { inventoryApi, facilitiesApi } from '@/lib/api';
import { InventoryTransaction, Facility } from '@/types';
import { Search, History, ArrowDownLeft, ArrowUpRight, ArrowLeftRight, RotateCcw } from 'lucide-react';
import Link from 'next/link';

export default function TransactionsLedgerPage() {
  const [transactions, setTransactions] = useState<InventoryTransaction[]>([]);
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<number | undefined>(undefined);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [facs, txs] = await Promise.all([
          facilitiesApi.list(),
          inventoryApi.listTransactions(selectedFacility),
        ]);
        setFacilities(facs);
        setTransactions(txs);
      } catch (err) {
        console.error('Failed to load transactions:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, [selectedFacility]);

  const filteredTransactions = transactions.filter((t) => {
    const q = searchQuery.toLowerCase();
    const medMatch = t.medicine_name?.toLowerCase().includes(q) || false;
    const refMatch = t.reference_number?.toLowerCase().includes(q) || false;
    return medMatch || refMatch;
  });

  const getTypeBadge = (type: string) => {
    switch (type.toLowerCase()) {
      case 'receipt':
        return (
          <Badge variant="success" className="gap-1">
            <ArrowDownLeft className="w-3 h-3" /> Receipt
          </Badge>
        );
      case 'issue':
        return (
          <Badge variant="danger" className="gap-1">
            <ArrowUpRight className="w-3 h-3" /> Issue
          </Badge>
        );
      case 'transfer in':
      case 'transfer out':
        return (
          <Badge variant="info" className="gap-1">
            <ArrowLeftRight className="w-3 h-3" /> {type}
          </Badge>
        );
      default:
        return (
          <Badge variant="default" className="gap-1">
            <RotateCcw className="w-3 h-3" /> {type}
          </Badge>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-slate-200/80 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Bin-Card Inventory Ledger
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Immutable audit trail of all receipts, issues, lateral transfers, and inventory adjustments.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search reference number or medicine..."
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
      </div>

      {/* Transactions Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
              <tr>
                <th className="px-6 py-3.5">Timestamp</th>
                <th className="px-6 py-3.5">Reference #</th>
                <th className="px-6 py-3.5">Medicine</th>
                <th className="px-6 py-3.5">Facility</th>
                <th className="px-6 py-3.5">Type</th>
                <th className="px-6 py-3.5">Quantity Change</th>
                <th className="px-6 py-3.5">Balance After</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredTransactions.map((tx) => (
                <tr key={tx.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="px-6 py-3.5 font-mono text-slate-500 text-[11px]">
                    {tx.created_at ? new Date(tx.created_at).toLocaleString() : '—'}
                  </td>
                  <td className="px-6 py-3.5 font-mono font-medium text-slate-800">
                    {tx.reference_number || `TX-${tx.id}`}
                  </td>
                  <td className="px-6 py-3.5 font-medium text-slate-900">
                    {tx.medicine_name || `Medicine #${tx.medicine_id}`}
                  </td>
                  <td className="px-6 py-3.5 text-slate-600">
                    {tx.facility_name || 'Tikur Anbessa Hospital'}
                  </td>
                  <td className="px-6 py-3.5">{getTypeBadge(tx.transaction_type)}</td>
                  <td className="px-6 py-3.5 font-semibold">
                    <span className={(tx.quantity ?? 0) > 0 ? 'text-emerald-600' : 'text-rose-600'}>
                      {(tx.quantity ?? 0) > 0 ? `+${tx.quantity}` : (tx.quantity ?? 0)}
                    </span>
                  </td>
                  <td className="px-6 py-3.5 font-bold text-slate-900">
                    {(tx.balance_after ?? 0).toLocaleString()}
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
