import React from 'react';
import Link from 'next/link';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex bg-slate-50">
      {/* Sidebar Navigation */}
      <aside className="w-64 border-r border-slate-200 bg-white flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-slate-200">
          <span className="font-bold text-lg text-blue-600 tracking-tight">PharmaIntelligence AI</span>
        </div>
        <nav className="flex-1 p-4 space-y-1 overflow-y-auto text-sm">
          <Link href="/dashboard" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Overview</Link>
          <Link href="/inventory" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Inventory</Link>
          <Link href="/forecasting" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Demand Forecasting</Link>
          <Link href="/stockout-intelligence" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Stockout Intelligence</Link>
          <Link href="/expiry-prevention" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Expiry Prevention</Link>
          <Link href="/redistribution" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Redistribution</Link>
          <Link href="/data-quality" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Data Quality</Link>
          <Link href="/ai-laboratory" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">AI Laboratory</Link>
          <Link href="/reports" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Reports</Link>
          <Link href="/notifications" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Notifications</Link>
          <div className="pt-4 border-t border-slate-200 my-2"></div>
          <Link href="/facilities" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Facilities</Link>
          <Link href="/users" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Users</Link>
          <Link href="/audit-logs" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Audit Logs</Link>
          <Link href="/settings" className="flex items-center px-3 py-2 rounded-md hover:bg-slate-100 font-medium text-slate-700">Settings</Link>
        </nav>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-800">Operational Console</h2>
          <div className="flex items-center gap-4">
            <span className="text-xs bg-emerald-100 text-emerald-800 px-2.5 py-1 rounded-full font-medium">System Online</span>
            <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-sm">
              PI
            </div>
          </div>
        </header>
        <main className="flex-1 p-6 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
