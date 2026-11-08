'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { inventoryApi, facilitiesApi } from '@/lib/api';
import { InventoryItem, Facility } from '@/types';
import {
  Package,
  Search,
  Filter,
  Plus,
  ArrowUpDown,
  AlertCircle,
  CheckCircle2,
  AlertTriangle,
  History,
} from 'lucide-react';
import Link from 'next/link';

export default function InventoryOverviewPage() {
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<number | undefined>(undefined);
  const [selectedStatus, setSelectedStatus] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  // New Transaction Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [txFacilityId, setTxFacilityId] = useState<number>(1);
  const [txMedicineId, setTxMedicineId] = useState<number>(1);
  const [txType, setTxType] = useState<string>('Receipt');
  const [txQty, setTxQty] = useState<number>(100);
  const [txRef, setTxRef] = useState<string>('BIN-2026-');
  const [txSubmitting, setTxSubmitting] = useState(false);

  useEffect(() => {
    async function loadData() {
      try {
        const [facs, inv] = await Promise.all([
          facilitiesApi.list(),
          inventoryApi.list(selectedFacility, selectedStatus === 'All' ? undefined : selectedStatus),
        ]);
        setFacilities(facs);
        setInventory(inv);
      } catch (err) {
        console.error('Failed to load inventory data:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, [selectedFacility, selectedStatus]);

  const filteredInventory = inventory.filter((item) => {
    const q = searchQuery.toLowerCase();
    const nameMatch = item.medicine_name?.toLowerCase().includes(q) || false;
    const codeMatch = item.medicine_code?.toLowerCase().includes(q) || false;
    return nameMatch || codeMatch;
  });

  const handleRecordTransaction = async (e: React.FormEvent) => {
    e.preventDefault();
    setTxSubmitting(true);
    try {
      await inventoryApi.recordTransaction({
        facility_id: txFacilityId,
        medicine_id: txMedicineId,
        transaction_type: txType,
        quantity: txType === 'Issue' ? -Math.abs(txQty) : Math.abs(txQty),
        reference_number: txRef,
      });
      setIsModalOpen(false);
      // Reload inventory
      const updated = await inventoryApi.list(selectedFacility, selectedStatus === 'All' ? undefined : selectedStatus);
      setInventory(updated);
    } catch (err: any) {
      alert(`Error recording transaction: ${err.message}`);
    } finally {
      setTxSubmitting(false);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status.toLowerCase()) {
      case 'adequate':
        return <Badge variant="success">Adequate</Badge>;
      case 'understocked':
        return <Badge variant="warning">Understocked</Badge>;
      case 'stockout':
        return <Badge variant="danger">Stockout</Badge>;
      default:
        return <Badge variant="default">{status}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Facility Inventory Ledger
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Real-time multi-echelon stock levels, buffer thresholds, and bin-card reconciliation.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link href="/inventory/transactions">
            <Button variant="outline" size="sm">
              <History className="w-3.5 h-3.5 mr-1.5" />
              Bin-Card Ledger
            </Button>
          </Link>
          <Button variant="primary" size="sm" onClick={() => setIsModalOpen(true)}>
            <Plus className="w-3.5 h-3.5 mr-1.5" />
            Record Transaction
          </Button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
        {/* Search Input */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search medicine or code..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Facility Dropdown */}
        <div>
          <select
            value={selectedFacility || ''}
            onChange={(e) => setSelectedFacility(e.target.value ? Number(e.target.value) : undefined)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="">All Ethiopian Facilities</option>
            {facilities.map((f) => (
              <option key={f.id} value={f.id}>
                {f.name} ({f.region})
              </option>
            ))}
          </select>
        </div>

        {/* Stock Status Filter */}
        <div>
          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="All">All Stock Statuses</option>
            <option value="Adequate">Adequate</option>
            <option value="Understocked">Understocked</option>
            <option value="Stockout">Stockout</option>
          </select>
        </div>
      </div>

      {/* Inventory Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
              <tr>
                <th className="px-6 py-3.5">Medicine Name</th>
                <th className="px-6 py-3.5">Facility</th>
                <th className="px-6 py-3.5">Stock Level</th>
                <th className="px-6 py-3.5">Reorder Point</th>
                <th className="px-6 py-3.5">Lead Time</th>
                <th className="px-6 py-3.5">Status</th>
                <th className="px-6 py-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredInventory.map((item) => (
                <tr key={item.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="px-6 py-3.5">
                    <div className="font-semibold text-slate-900">{item.medicine_name}</div>
                    <div className="text-[10px] text-slate-400 font-mono mt-0.5">{item.medicine_code}</div>
                  </td>
                  <td className="px-6 py-3.5 text-slate-600">
                    {item.facility_name || 'Tikur Anbessa Hospital'}
                  </td>
                  <td className="px-6 py-3.5 font-medium">
                    <span className={item.current_quantity === 0 ? 'text-rose-600 font-bold' : 'text-slate-900'}>
                      {item.current_quantity.toLocaleString()} units
                    </span>
                  </td>
                  <td className="px-6 py-3.5 text-slate-600">
                    {item.reorder_level.toLocaleString()} units
                  </td>
                  <td className="px-6 py-3.5 text-slate-600">
                    {item.lead_time_days} days
                  </td>
                  <td className="px-6 py-3.5">
                    {getStatusBadge(item.stock_status)}
                  </td>
                  <td className="px-6 py-3.5 text-right space-x-2">
                    <Link
                      href={`/forecasting?facility_id=${item.facility_id}&medicine_id=${item.medicine_id}`}
                      className="text-blue-600 hover:text-blue-800 font-medium"
                    >
                      Forecast
                    </Link>
                  </td>
                </tr>
              ))}
              {filteredInventory.length === 0 && !isLoading && (
                <tr>
                  <td colSpan={7} className="px-6 py-8 text-center text-slate-400">
                    No matching inventory items found for current filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Quick Add Transaction Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
          <div className="w-full max-w-md bg-white rounded-xl shadow-xl border border-slate-200 p-6 space-y-4">
            <h3 className="text-base font-bold text-slate-900">Record Bin-Card Transaction</h3>
            <form onSubmit={handleRecordTransaction} className="space-y-3 text-xs">
              <div>
                <label className="block font-medium text-slate-700 mb-1">Facility</label>
                <select
                  value={txFacilityId}
                  onChange={(e) => setTxFacilityId(Number(e.target.value))}
                  className="w-full px-3 py-1.5 border rounded-lg bg-slate-50 focus:bg-white"
                >
                  {facilities.map((f) => (
                    <option key={f.id} value={f.id}>
                      {f.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-medium text-slate-700 mb-1">Transaction Type</label>
                <select
                  value={txType}
                  onChange={(e) => setTxType(e.target.value)}
                  className="w-full px-3 py-1.5 border rounded-lg bg-slate-50 focus:bg-white"
                >
                  <option value="Receipt">Receipt (Stock In)</option>
                  <option value="Issue">Issue (Dispensing)</option>
                  <option value="Adjustment">Inventory Adjustment</option>
                </select>
              </div>

              <div>
                <label className="block font-medium text-slate-700 mb-1">Quantity</label>
                <input
                  type="number"
                  value={txQty}
                  onChange={(e) => setTxQty(Number(e.target.value))}
                  required
                  min={1}
                  className="w-full px-3 py-1.5 border rounded-lg bg-slate-50 focus:bg-white"
                />
              </div>

              <div>
                <label className="block font-medium text-slate-700 mb-1">Reference Number</label>
                <input
                  type="text"
                  value={txRef}
                  onChange={(e) => setTxRef(e.target.value)}
                  required
                  className="w-full px-3 py-1.5 border rounded-lg bg-slate-50 focus:bg-white"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => setIsModalOpen(false)}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  size="sm"
                  isLoading={txSubmitting}
                >
                  Save Transaction
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
