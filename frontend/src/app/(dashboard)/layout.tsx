'use client';

import React, { useState, useRef, useEffect } from 'react';
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
  ChevronLeft,
  Shield,
  Activity,
  Menu,
  X,
  Cpu,
  Users,
  ShieldCheck,
  Settings as SettingsIcon,
  Bell,
  Sparkles,
  ExternalLink,
  Info,
  UploadCloud,
} from 'lucide-react';
import Tooltip from '@/components/ui/Tooltip';

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
      { name: 'Data & Ledger Import', href: '/inventory/import', icon: UploadCloud },
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

const QUICK_ALERTS = [
  {
    id: 1,
    title: 'Critical Stockout: Amoxicillin 500mg',
    facility: 'Jimma University Medical Center',
    severity: 'critical',
    time: '12m ago',
    href: '/stockout-intelligence',
  },
  {
    id: 2,
    title: 'Impending Expiry: Artemether-Lumefantrine',
    facility: 'Tikur Anbessa Specialized Hospital',
    severity: 'high',
    time: '45m ago',
    href: '/expiry-prevention',
  },
  {
    id: 3,
    title: 'MILP Transfer Route Formulated',
    facility: "St. Paul's MMC -> Hawassa Referral",
    severity: 'info',
    time: '2h ago',
    href: '/redistribution',
  },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [desktopCollapsed, setDesktopCollapsed] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const notifRef = useRef<HTMLDivElement>(null);

  // Close notifications on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (notifRef.current && !notifRef.current.contains(event.target as Node)) {
        setNotificationsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const isActive = (href: string) => {
    if (href === '/dashboard') return pathname === '/dashboard';
    return pathname.startsWith(href);
  };

  return (
    <div className="h-screen w-screen overflow-hidden flex bg-slate-50 text-slate-900 font-sans">
      {/* Mobile Backdrop */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/60 backdrop-blur-xs lg:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar Navigation */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 h-screen bg-slate-900 text-slate-100 flex flex-col border-r border-slate-800 transition-all duration-200 lg:translate-x-0 ${
          mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:static lg:h-screen lg:shrink-0 ${desktopCollapsed ? 'lg:w-20' : 'lg:w-64'} w-64`}
      >
        {/* Brand Header */}
        <div className="h-16 flex items-center justify-between px-4 sm:px-6 border-b border-slate-800 bg-slate-950/40">
          <Link href="/dashboard" className="flex items-center gap-2.5 overflow-hidden">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20 shrink-0">
              <Shield className="w-4 h-4" />
            </div>
            {!desktopCollapsed && (
              <div className="truncate">
                <span className="font-bold text-base tracking-tight text-white block truncate">
                  PharmaIntelligence
                </span>
                <span className="text-[10px] block text-blue-400 font-medium -mt-1 tracking-wider uppercase truncate">
                  Ethiopian Health DSS
                </span>
              </div>
            )}
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
              {!desktopCollapsed && (
                <div className="px-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5 truncate">
                  {section.title}
                </div>
              )}
              {section.items.map((item) => {
                const active = isActive(item.href);
                const Icon = item.icon;
                return (
                  <Link
                    key={item.href}
                    href={item.href as any}
                    onClick={() => setMobileMenuOpen(false)}
                    title={desktopCollapsed ? item.name : undefined}
                    className={`flex items-center ${desktopCollapsed ? 'justify-center px-2' : 'justify-between px-3'} py-2 text-xs font-medium rounded-lg transition-all ${
                      active
                        ? 'bg-blue-600 text-white font-semibold shadow-xs'
                        : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                    }`}
                  >
                    <div className="flex items-center gap-2.5 truncate">
                      <Icon className={`w-4 h-4 shrink-0 ${active ? 'text-white' : 'text-slate-400'}`} />
                      {!desktopCollapsed && <span className="truncate">{item.name}</span>}
                    </div>
                    {!desktopCollapsed && item.badge && (
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

        {/* Desktop Collapse Toggle */}
        <div className="hidden lg:flex items-center justify-end px-3 py-2 border-t border-slate-800/80">
          <button
            onClick={() => setDesktopCollapsed(!desktopCollapsed)}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            title={desktopCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
          >
            {desktopCollapsed ? (
              <ChevronRight className="w-4 h-4" />
            ) : (
              <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
                <ChevronLeft className="w-3.5 h-3.5" />
                <span>Collapse</span>
              </div>
            )}
          </button>
        </div>

        {/* User Card & Logout in Sidebar Footer */}
        <div className="p-3 border-t border-slate-800 bg-slate-950/60">
          <div className="flex items-center justify-between p-2 rounded-lg bg-slate-800/60 border border-slate-700/60">
            <div className="flex items-center gap-2.5 overflow-hidden">
              <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xs shrink-0">
                {user?.full_name?.charAt(0) || 'U'}
              </div>
              {!desktopCollapsed && (
                <div className="truncate">
                  <div className="text-xs font-semibold text-white truncate">
                    {user?.full_name || 'System User'}
                  </div>
                  <div className="text-[10px] text-blue-400 font-medium capitalize truncate">
                    {user?.role?.replace(/_/g, ' ') || 'Healthcare Staff'}
                  </div>
                </div>
              )}
            </div>
            {!desktopCollapsed && (
              <button
                onClick={() => logout()}
                title="Logout"
                className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-md transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-screen min-w-0 overflow-hidden">
        {/* Top Header */}
        <header className="h-16 shrink-0 bg-white border-b border-slate-200 px-4 sm:px-6 flex items-center justify-between z-30 shadow-xs">
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

          <div className="flex items-center gap-2.5 sm:gap-3">
            {/* Research Environment Badge */}
            <Tooltip content="Synthetic research testbed calibrated to Ethiopian Health Tier protocols. Real patient records are not stored.">
              <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200 text-xs font-medium cursor-help">
                <Sparkles className="w-3.5 h-3.5 text-blue-600" />
                <span>Demonstration Sandbox</span>
              </div>
            </Tooltip>

            {/* Simulation Node Badge */}
            <Tooltip content="Discrete-event simulation engine active for multi-facility demand and lead time distribution.">
              <div className="flex items-center gap-2 px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-medium cursor-help">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span className="hidden sm:inline">Simulation Node</span> Active
              </div>
            </Tooltip>

            {/* Notifications Dropdown Container */}
            <div className="relative" ref={notifRef}>
              <button
                onClick={() => setNotificationsOpen(!notificationsOpen)}
                className={`p-2 rounded-lg transition-colors relative ${
                  notificationsOpen ? 'bg-slate-100 text-slate-900' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'
                }`}
                title="Notifications"
                aria-expanded={notificationsOpen}
              >
                <Bell className="w-4 h-4" />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-rose-500 rounded-full"></span>
              </button>

              {/* Notification Popover Dropdown */}
              {notificationsOpen && (
                <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-white rounded-xl shadow-xl border border-slate-200 py-3 z-50 text-xs">
                  <div className="flex items-center justify-between px-4 pb-2 border-b border-slate-100">
                    <div className="font-semibold text-slate-900 flex items-center gap-1.5">
                      <Bell className="w-3.5 h-3.5 text-blue-600" /> Priority Alerts
                    </div>
                    <span className="text-[10px] bg-rose-100 text-rose-700 font-bold px-1.5 py-0.5 rounded">
                      3 Unresolved
                    </span>
                  </div>

                  <div className="divide-y divide-slate-100 max-h-72 overflow-y-auto">
                    {QUICK_ALERTS.map((alert) => (
                      <Link
                        key={alert.id}
                        href={alert.href as any}
                        onClick={() => setNotificationsOpen(false)}
                        className="block px-4 py-2.5 hover:bg-slate-50 transition"
                      >
                        <div className="flex items-center justify-between">
                          <span
                            className={`px-1.5 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider ${
                              alert.severity === 'critical'
                                ? 'bg-rose-100 text-rose-800'
                                : alert.severity === 'high'
                                ? 'bg-amber-100 text-amber-800'
                                : 'bg-blue-100 text-blue-800'
                            }`}
                          >
                            {alert.severity}
                          </span>
                          <span className="text-[10px] text-slate-400">{alert.time}</span>
                        </div>
                        <div className="font-semibold text-slate-900 mt-1 truncate">
                          {alert.title}
                        </div>
                        <div className="text-[11px] text-slate-500 mt-0.5 truncate">
                          {alert.facility}
                        </div>
                      </Link>
                    ))}
                  </div>

                  <div className="px-4 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px]">
                    <span className="text-slate-400">Alert dispatch channel active</span>
                    <Link
                      href="/notifications"
                      onClick={() => setNotificationsOpen(false)}
                      className="text-blue-600 hover:text-blue-700 font-semibold flex items-center gap-1"
                    >
                      View all alerts <ChevronRight className="w-3 h-3" />
                    </Link>
                  </div>
                </div>
              )}
            </div>

            {/* Current Facility Badge */}
            <div className="text-right hidden xl:block border-l border-slate-200 pl-3">
              <div className="text-xs font-semibold text-slate-900 truncate max-w-[200px]">
                {user?.facility_name || 'Tikur Anbessa Specialized Hospital'}
              </div>
              <div className="text-[11px] text-slate-500">
                Facility Code: {user?.facility_id ? `ETH-FAC-${user.facility_id}` : 'ETH-ADD-TASH'}
              </div>
            </div>
          </div>
        </header>

        {/* Main Body */}
        <main className="flex-1 p-4 sm:p-6 md:p-8 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
