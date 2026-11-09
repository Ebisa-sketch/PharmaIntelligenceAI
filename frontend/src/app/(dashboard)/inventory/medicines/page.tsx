'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { medicinesApi } from '@/lib/api';
import { Medicine } from '@/types';
import { Search, Layers, Pill, ShieldCheck, Filter } from 'lucide-react';
import Link from 'next/link';

export default function MedicinesCatalogPage() {
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedVital, setSelectedVital] = useState<string>('All');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadMedicines() {
      try {
        const data = await medicinesApi.list();
        setMedicines(data);
      } catch (err) {
        console.error('Failed to load medicines:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadMedicines();
  }, []);

  const categories = Array.from(new Set(medicines.map((m) => m.category))).filter(Boolean);

  const filteredMedicines = medicines.filter((m) => {
    const q = searchQuery.toLowerCase();
    const nameMatch = m.name.toLowerCase().includes(q) || m.code.toLowerCase().includes(q);
    const categoryMatch = selectedCategory === 'All' || m.category === selectedCategory;
    const vitalMatch = selectedVital === 'All' || m.vital_classification === selectedVital;
    return nameMatch && categoryMatch && vitalMatch;
  });

  const getVitalBadge = (classification: string) => {
    switch (classification) {
      case 'Vital':
        return <Badge variant="danger">Vital (Life-Saving)</Badge>;
      case 'Essential':
        return <Badge variant="warning">Essential</Badge>;
      default:
        return <Badge variant="default">Non-Essential</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-slate-200/80 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Ethiopian National Essential Medicines List (NEML)
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Standardized therapeutic formulary, vital classification, and safety stock parameters.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
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

        <div>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="All">All Therapeutic Categories</option>
            {categories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>

        <div>
          <select
            value={selectedVital}
            onChange={(e) => setSelectedVital(e.target.value)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="All">All VED Classifications</option>
            <option value="Vital">Vital</option>
            <option value="Essential">Essential</option>
            <option value="Non-essential">Non-Essential</option>
          </select>
        </div>
      </div>

      {/* Medicines Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
              <tr>
                <th className="px-6 py-3.5">Code</th>
                <th className="px-6 py-3.5">Generic Name</th>
                <th className="px-6 py-3.5">Category</th>
                <th className="px-6 py-3.5">Dosage / Strength</th>
                <th className="px-6 py-3.5">VED Category</th>
                <th className="px-6 py-3.5">Min Stock Buffer</th>
                <th className="px-6 py-3.5">Lead Time</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredMedicines.map((m) => (
                <tr key={m.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="px-6 py-3.5 font-mono text-[11px] font-medium text-slate-500">
                    {m.code}
                  </td>
                  <td className="px-6 py-3.5">
                    <div className="font-semibold text-slate-900">{m.name}</div>
                    {m.brand_name && (
                      <div className="text-[10px] text-slate-400">Brand: {m.brand_name}</div>
                    )}
                  </td>
                  <td className="px-6 py-3.5 text-slate-600">{m.category}</td>
                  <td className="px-6 py-3.5 text-slate-600">
                    {m.dosage_form} ({m.strength})
                  </td>
                  <td className="px-6 py-3.5">{getVitalBadge(m.vital_classification)}</td>
                  <td className="px-6 py-3.5 font-medium text-slate-800">
                    {(m.minimum_stock_level ?? 0).toLocaleString()} {m.unit_of_measure}
                  </td>
                  <td className="px-6 py-3.5 text-slate-600">{m.lead_time_days ?? 0} days</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
