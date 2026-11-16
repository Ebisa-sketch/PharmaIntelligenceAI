'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { DemoAlert } from '@/components/ui/DemoAlert';
import { Pagination } from '@/components/ui/Pagination';
import { EmptyState } from '@/components/ui/EmptyState';
import { usersApi, facilitiesApi } from '@/lib/api';
import { User, Facility } from '@/types';
import {
  Users,
  UserPlus,
  Search,
  Shield,
  Building2,
  Mail,
  CheckCircle2,
  XCircle,
  MoreVertical,
  X,
  Lock,
} from 'lucide-react';

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRole, setSelectedRole] = useState('All');
  const [selectedFacility, setSelectedFacility] = useState('All');
  const [isLoading, setIsLoading] = useState(true);

  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 8;

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newFullName, setNewFullName] = useState('');
  const [newEmail, setNewEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newRole, setNewRole] = useState('pharmacist');
  const [newFacilityId, setNewFacilityId] = useState<number>(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [usersData, facsData] = await Promise.all([
          usersApi.list(),
          facilitiesApi.list(),
        ]);
        setUsers(usersData);
        setFacilities(facsData);
      } catch (err) {
        console.error('Failed to load users:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setActionSuccess(null);
    try {
      const selectedFac = facilities.find((f) => f.id === newFacilityId);
      const created = await usersApi.create({
        full_name: newFullName,
        email: newEmail,
        password: newPassword || 'Password123!',
        role: newRole,
        facility_id: newFacilityId,
      });

      const enrichedUser: User = {
        ...created,
        facility_name: selectedFac?.name || 'Assigned Facility',
      };

      setUsers((prev) => [enrichedUser, ...prev]);
      setActionSuccess(`User ${newFullName} provisioned successfully with role ${newRole}.`);
      setIsModalOpen(false);
      setNewFullName('');
      setNewEmail('');
      setNewPassword('');
    } catch (err: any) {
      alert(`User creation failed: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const filteredUsers = users.filter((u) => {
    const q = searchQuery.toLowerCase();
    const matchesSearch =
      u.full_name.toLowerCase().includes(q) ||
      u.email.toLowerCase().includes(q) ||
      (u.facility_name && u.facility_name.toLowerCase().includes(q));
    const matchesRole = selectedRole === 'All' || u.role.toLowerCase() === selectedRole.toLowerCase();
    const matchesFacility =
      selectedFacility === 'All' || String(u.facility_id) === selectedFacility;
    return matchesSearch && matchesRole && matchesFacility;
  });

  const totalPages = Math.ceil(filteredUsers.length / itemsPerPage);
  const displayedUsers = filteredUsers.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const getRoleBadge = (role: string) => {
    switch (role.toLowerCase()) {
      case 'admin':
        return <Badge variant="danger">System Admin</Badge>;
      case 'pharmacist':
        return <Badge variant="info">Hospital Pharmacist</Badge>;
      case 'inventory_manager':
        return <Badge variant="warning">Inventory Manager</Badge>;
      case 'clinical_director':
        return <Badge variant="purple">Clinical Director</Badge>;
      case 'data_officer':
        return <Badge variant="default">Data Officer</Badge>;
      default:
        return <Badge variant="default">{role}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            User &amp; Access Administration
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Role-Based Access Control (RBAC), facility tenant boundaries, and credential provisioning.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="primary" size="sm" onClick={() => setIsModalOpen(true)}>
            <UserPlus className="w-3.5 h-3.5 mr-1.5" />
            Provision New User
          </Button>
        </div>
      </div>

      <DemoAlert
        title="Multi-Tenant Access Isolation"
        message="Users are bound to specific Ethiopian healthcare facilities under strict multi-tenant authorization barriers. Only System Administrators possess cross-facility national visibility."
      />

      {actionSuccess && (
        <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-2 shadow-2xs">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{actionSuccess}</span>
        </div>
      )}

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Total Provisioned Users
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-1">{users.length} Users</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Across {facilities.length} network facilities</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Active Hospital Accounts
          </div>
          <div className="text-2xl font-bold text-emerald-600 mt-1">
            {users.filter((u) => u.is_active).length} Active
          </div>
          <div className="text-[11px] text-emerald-700 mt-0.5">Compliant with active MFA tokens</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Clinical Directors &amp; Admins
          </div>
          <div className="text-2xl font-bold text-purple-600 mt-1">
            {users.filter((u) => ['admin', 'clinical_director'].includes(u.role.toLowerCase())).length}
          </div>
          <div className="text-[11px] text-purple-700 mt-0.5">Authorized for transfer approvals</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Security Authentication
          </div>
          <div className="text-2xl font-bold text-blue-600 mt-1">JWT + Argon2id</div>
          <div className="text-[11px] text-blue-700 mt-0.5">Zero plain-text password storage</div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 bg-white p-4 rounded-xl border border-slate-200/80 shadow-2xs">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search user name, email, facility..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <select
            value={selectedRole}
            onChange={(e) => setSelectedRole(e.target.value)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="All">All User Roles</option>
            <option value="admin">System Administrator</option>
            <option value="pharmacist">Hospital Pharmacist</option>
            <option value="inventory_manager">Inventory Manager</option>
            <option value="clinical_director">Clinical Director</option>
            <option value="data_officer">Data Quality Officer</option>
          </select>
        </div>

        <div>
          <select
            value={selectedFacility}
            onChange={(e) => setSelectedFacility(e.target.value)}
            className="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
          >
            <option value="All">All Associated Facilities</option>
            {facilities.map((f) => (
              <option key={f.id} value={String(f.id)}>
                {f.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Users Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-2xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
              <tr>
                <th className="px-6 py-3.5">User Identity</th>
                <th className="px-6 py-3.5">Assigned Facility</th>
                <th className="px-6 py-3.5">RBAC Role</th>
                <th className="px-6 py-3.5">Account Status</th>
                <th className="px-6 py-3.5">Provisioned Date</th>
                <th className="px-6 py-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {displayedUsers.map((u) => (
                <tr key={u.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="px-6 py-3.5">
                    <div className="font-semibold text-slate-900">{u.full_name}</div>
                    <div className="text-[11px] text-slate-500 flex items-center gap-1 mt-0.5">
                      <Mail className="w-3 h-3 text-slate-400" />
                      <span>{u.email}</span>
                    </div>
                  </td>
                  <td className="px-6 py-3.5 text-slate-700 font-medium">
                    {u.facility_name || 'Tikur Anbessa Hospital'}
                  </td>
                  <td className="px-6 py-3.5">{getRoleBadge(u.role)}</td>
                  <td className="px-6 py-3.5">
                    {u.is_active ? (
                      <span className="inline-flex items-center gap-1 text-emerald-700 font-medium text-[11px]">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Active
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-slate-400 font-medium text-[11px]">
                        <XCircle className="w-3.5 h-3.5 text-slate-400" /> Deactivated
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-3.5 text-slate-500 font-mono text-[11px]">
                    {u.created_at ? new Date(u.created_at).toLocaleDateString() : '2026-01-15'}
                  </td>
                  <td className="px-6 py-3.5 text-right">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => alert(`Viewing access permissions for: ${u.full_name}`)}
                    >
                      Permissions
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredUsers.length === 0 && !isLoading && (
          <EmptyState
            icon={Users}
            title="No Users Found"
            description="No user accounts matched your search and filter criteria."
            actionLabel="Reset Filters"
            onAction={() => {
              setSearchQuery('');
              setSelectedRole('All');
              setSelectedFacility('All');
            }}
          />
        )}

        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
          totalItems={filteredUsers.length}
          itemsPerPage={itemsPerPage}
        />
      </div>

      {/* Provision User Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
          <div className="w-full max-w-md bg-white rounded-xl shadow-xl border border-slate-200 p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <UserPlus className="w-4 h-4 text-blue-600" />
                <h3 className="text-base font-bold text-slate-900">Provision Healthcare User</h3>
              </div>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleCreateUser} className="space-y-3.5 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Full Legal Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Dr. Aster Kebede"
                  value={newFullName}
                  onChange={(e) => setNewFullName(e.target.value)}
                  className="w-full px-3 py-1.5 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Institutional Email</label>
                <input
                  type="email"
                  required
                  placeholder="e.g. aster.kebede@pharmaintelligence.et"
                  value={newEmail}
                  onChange={(e) => setNewEmail(e.target.value)}
                  className="w-full px-3 py-1.5 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Temporary Initial Password</label>
                <input
                  type="password"
                  required
                  placeholder="Minimum 8 characters"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="w-full px-3 py-1.5 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Healthcare RBAC Role</label>
                <select
                  value={newRole}
                  onChange={(e) => setNewRole(e.target.value)}
                  className="w-full px-3 py-1.5 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white text-slate-800"
                >
                  <option value="pharmacist">Hospital Pharmacist (Dispensing &amp; FEFO)</option>
                  <option value="inventory_manager">Inventory Manager (Bin-cards &amp; Receipts)</option>
                  <option value="clinical_director">Clinical Director (Approvals &amp; Transfers)</option>
                  <option value="data_officer">Data Quality Officer (Cleansing &amp; Ingestion)</option>
                  <option value="admin">System Administrator (Full Tenant Privileges)</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Assigned Facility</label>
                <select
                  value={newFacilityId}
                  onChange={(e) => setNewFacilityId(Number(e.target.value))}
                  className="w-full px-3 py-1.5 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white text-slate-800"
                >
                  {facilities.map((f) => (
                    <option key={f.id} value={f.id}>
                      {f.name} ({f.region})
                    </option>
                  ))}
                </select>
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
                  isLoading={isSubmitting}
                >
                  Provision User
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
