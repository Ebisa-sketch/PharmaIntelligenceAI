'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { facilitiesApi } from '@/lib/api';
import { Facility } from '@/types';
import { Building2, Search, MapPin, HardDrive, CheckCircle2 } from 'lucide-react';

export default function FacilitiesDirectoryPage() {
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('All');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadFacilities() {
      try {
        const data = await facilitiesApi.list();
        setFacilities(data);
      } catch (err) {
        console.error('Failed to load facilities:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadFacilities();
  }, []);

  const regions = Array.from(new Set(facilities.map((f) => f.region))).filter(Boolean);

  const filteredFacilities = facilities.filter((f) => {
    const q = searchQuery.toLowerCase();
    const matchQuery =
      f.name.toLowerCase().includes(q) ||
      f.code.toLowerCase().includes(q) ||
      f.region.toLowerCase().includes(q);
    const matchRegion = selectedRegion === 'All' || f.region === selectedRegion;
    return matchQuery && matchRegion;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-slate-200/80 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Ethiopian Healthcare Facilities Directory
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Geographic coordination, warehousing capacity, and cold-chain infrastructure across regional health networks.
        </p>
      </div>

      {/* Filter and Search */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search facility name, code, or city..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="All">All Regions</option>
            {regions.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Facilities Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredFacilities.map((f) => (
          <div
            key={f.id}
            className="p-5 bg-white rounded-xl border border-slate-200/80 shadow-xs hover:border-blue-300 transition-colors space-y-3"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="space-y-1">
                <span className="font-mono text-[10px] text-blue-600 bg-blue-50 px-2 py-0.5 rounded font-semibold border border-blue-200">
                  {f.code}
                </span>
                <h3 className="font-bold text-slate-900 text-sm">{f.name}</h3>
                <div className="text-xs text-slate-500 font-medium">{f.facility_type}</div>
              </div>
              <Badge variant={f.is_active ? 'success' : 'default'}>
                {f.is_active ? 'Online' : 'Inactive'}
              </Badge>
            </div>

            <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-100 text-xs text-slate-600">
              <div className="flex items-center gap-1.5">
                <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                <span className="truncate">
                  {f.zone ? `${f.zone}, ` : ''}{f.region}
                </span>
              </div>
              <div className="flex items-center gap-1.5">
                <HardDrive className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                <span>{(f.storage_capacity_m3 ?? 0).toLocaleString()} m³ capacity</span>
              </div>
            </div>

            <div className="text-[11px] text-slate-400 font-mono">
              GPS Coordinates: {(f.latitude ?? 0).toFixed(4)}°N, {(f.longitude ?? 0).toFixed(4)}°E
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
