'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import {
  LayoutDashboard,
  Package,
  Layers,
  CalendarClock,
  History,
  TrendingUp,
  AlertTriangle,
  Clock,
  RefreshCw,
  CheckCircle2,
  Building2,
  FileBarChart2,
  LogOut,
  ChevronRight,
  Shield,
  Activity,
  Menu,
  X,
  Cpu,
  Users,
  ShieldCheck,
  Settings as SettingsIcon,
  Bell,
  Search,
  Sparkles,
} from 'lucide-react';

interface NavItem {
  name: string;
  href: string;
  icon: React.ElementType;
  badge?: string;
  roles?: string[];
}

const navSections: { title: string; items: NavItem[] }[] = [
  {
    title: 'Operations & Stock',
    items: [
      { name: 'Executive Overview', href: '/dashboard', icon: LayoutDashboard },
      { name: 'Medicine Inventory', href: '/inventory', icon: Package },
      { name: 'NEML Medicines', href: '/inventory/medicines', icon: Layers },
      { name: 'Batch Lot Tracking', href: '/inventory/batches', icon: CalendarClock },
      { name: 'Bin-Card Transactions', href: '/inventory/transactions', icon: History },
    ],
  },
  {
    title: 'AI Decision Engines',
    items: [
      { name: 'Demand Forecasting', href: '/forecasting', icon: TrendingUp },
      { name: 'Stockout Intelligence', href: '/stockout-intelligence', icon: AlertTriangle, badge: 'Live' },
      { name: 'Expiry Prevention', href: '/expiry-prevention', icon: Clock },
      { name: 'Redistribution Optimizer', href: '/redistribution', icon: RefreshCw, badge: 'MILP' },
      { name: 'AI Model Laboratory', href: '/ai-laboratory', icon: Cpu, badge: 'Research' },
    ],
  },
  {
    title: 'Governance & Analytics',
    items: [
      { name: 'Data Quality (DQI)', href: '/data-quality', icon: CheckCircle2 },
      { name: 'Reports & Analytics', href: '/reports', icon: FileBarChart2 },
      { name: 'Audit & Compliance', href: '/audit-logs', icon: ShieldCheck },
    ],
  },
  {
    title: 'Administration',
    items: [
      { name: 'Facilities Directory', href: '/facilities', icon: Building2 },
      { name: 'User Management', href: '/users', icon: Users, roles: ['admin'] },
      { name: 'System Settings', href: '/settings', icon: SettingsIcon },
    ],
  },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const isActive = (href: string) => {
    if (href === '/dashboard') return pathname === '/dashboard';
    return pathname.startsWith(href);
  };

  return (
    <div className="min-h-screen flex bg-slate-50 text-slate-900 font-sans">
      {/* Mobile Backdrop */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/60 backdrop-blur-xs lg:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar Navigation */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-slate-900 text-slate-100 flex flex-col border-r border-slate-800 transition-transform duration-200 lg:translate-x-0 ${
          mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:static`}
      >
        {/* Brand Header */}
        <div className="h-16 flex items-center justify-between px-6 border-b border-slate-800 bg-slate-950/40">
          <Link href="/dashboard" className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
              <Shield className="w-4 h-4" />
            </div>
            <div>
              <span className="font-bold text-base tracking-tight text-white">PharmaIntelligence</span>
              <span className="text-[10px] block text-blue-400 font-medium -mt-1 tracking-wider uppercase">
                AI Ethiopian Health
              </span>
            </div>
          </Link>
          <button
            onClick={() => setMobileMenuOpen(false)}
            className="text-slate-400 hover:text-white lg:hidden"
            aria-label="Close Sidebar"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 px-3 py-4 space-y-5 overflow-y-auto">
          {navSections.map((section) => (
            <div key={section.title} className="space-y-1">
              <div className="px-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                {section.title}
              </div>
              {section.items.map((item) => {
                const active = isActive(item.href);
                const Icon = item.icon;
                return (
                  <Link
                    key={item.href}
                    href={item.href as any}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`flex items-center justify-between px-3 py-2 text-xs font-medium rounded-lg transition-all ${
                      active
                        ? 'bg-blue-600 text-white font-semibold shadow-xs'
                        : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                    }`}
                  >
                    <div className="flex items-center gap-2.5 truncate">
                      <Icon className={`w-4 h-4 shrink-0 ${active ? 'text-white' : 'text-slate-400'}`} />
                      <span className="truncate">{item.name}</span>
                    </div>
                    {item.badge && (
                      <span
                        className={`text-[10px] px-1.5 py-0.5 rounded font-bold ${
                          active
                            ? 'bg-white/20 text-white'
                            : 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                        }`}
                      >
                        {item.badge}
                      </span>
                    )}
                  </Link>
                );
              })}
            </div>
          ))}
        </nav>

        {/* User Card & Logout in Sidebar Footer */}
        <div className="p-3 border-t border-slate-800 bg-slate-950/60">
          <div className="flex items-center justify-between p-2 rounded-lg bg-slate-800/60 border border-slate-700/60">
            <div className="flex items-center gap-2.5 overflow-hidden">
              <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xs shrink-0">
                {user?.full_name?.charAt(0) || 'U'}
              </div>
              <div className="truncate">
                <div className="text-xs font-semibold text-white truncate">
                  {user?.full_name || 'System User'}
                </div>
                <div className="text-[10px] text-blue-400 font-medium capitalize">
                  {user?.role?.replace(/_/g, ' ') || 'Healthcare Staff'}
                </div>
              </div>
            </div>
            <button
              onClick={() => logout()}
              title="Logout"
              className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-md transition-colors"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Header */}
        <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between sticky top-0 z-30 shadow-xs">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setMobileMenuOpen(true)}
              className="p-2 -ml-2 text-slate-600 hover:text-slate-900 lg:hidden"
              aria-label="Open Sidebar"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <span className="font-semibold text-slate-800">Operational Console</span>
              <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
              <span className="text-slate-600 capitalize font-medium">
                {pathname.split('/')[1]?.replace(/-/g, ' ') || 'Dashboard'}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200 text-xs font-medium">
              <Sparkles className="w-3.5 h-3.5 text-blue-600" />
              <span>Pilot Demonstration System</span>
            </div>

            <div className="flex items-center gap-2 px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="hidden sm:inline">EPSS Network</span> Live
            </div>

            <Link
              href="/notifications"
              className="p-2 text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors relative"
              title="Notifications"
            >
              <Bell className="w-4 h-4" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-rose-500 rounded-full"></span>
            </Link>

            <div className="text-right hidden lg:block border-l border-slate-200 pl-3">
              <div className="text-xs font-semibold text-slate-900 truncate max-w-[200px]">
                {user?.facility_name || 'Tikur Anbessa Specialized Hospital'}
              </div>
              <div className="text-[11px] text-slate-500">
                Facility ID: #{user?.facility_id || '1'}
              </div>
            </div>
          </div>
        </header>

        {/* Main Body */}
        <main className="flex-1 p-6 md:p-8 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}

