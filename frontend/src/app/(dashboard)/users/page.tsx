export default function UsersPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">User Management</h1>
        <p className="text-sm text-slate-500 mt-1">Role-based access control (RBAC), user provisioning, and facility assignments.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Active Users</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">64</div>
          <div className="text-xs text-emerald-600 mt-1">Pharmacists, Logistics, Admins</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Pending Invites</div>
          <div className="text-2xl font-bold text-blue-600 mt-2">3</div>
          <div className="text-xs text-slate-500 mt-1">Invited via enterprise SSO</div>
        </div>
        <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">MFA Adoption</div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">100%</div>
          <div className="text-xs text-emerald-700 mt-1">Mandatory security policy active</div>
        </div>
      </div>
    </div>
  );
}
