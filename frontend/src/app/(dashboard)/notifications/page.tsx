'use client';

import { useState } from 'react';
import { 
  Bell, 
  AlertTriangle, 
  AlertCircle, 
  CheckCircle2, 
  Info, 
  Filter, 
  Check, 
  Trash2,
  ExternalLink,
  ShieldAlert,
  Send
} from 'lucide-react';
import DemoAlert from '@/components/ui/DemoAlert';

interface NotificationItem {
  id: string;
  title: string;
  message: string;
  severity: 'critical' | 'high' | 'medium' | 'info';
  timestamp: string;
  facility: string;
  category: 'Stockout' | 'Expiry' | 'Quality' | 'Redistribution' | 'Model';
  isRead: boolean;
  actionUrl?: string;
}

const INITIAL_NOTIFICATIONS: NotificationItem[] = [
  {
    id: 'notif-1',
    title: 'Critical Stockout Alert: Amoxicillin 500mg',
    message: 'Stock level at Jimma University Medical Center has fallen below safety buffer (0.8 DSR). Immediate replenishment or inter-facility transfer required.',
    severity: 'critical',
    timestamp: '12 minutes ago',
    facility: 'Jimma University Medical Center',
    category: 'Stockout',
    isRead: false,
    actionUrl: '/stockout-intelligence'
  },
  {
    id: 'notif-2',
    title: 'Impending Expiry Risk: Artemether-Lumefantrine',
    message: 'Batch B-AL-9024 (1,200 blisters) at Tikur Anbessa Specialized Hospital is expiring in 42 days with Projected Under-Utilization of 840 units.',
    severity: 'high',
    timestamp: '1 hour ago',
    facility: 'Tikur Anbessa Specialized Hospital',
    category: 'Expiry',
    isRead: false,
    actionUrl: '/expiry-prevention'
  },
  {
    id: 'notif-3',
    title: 'Redistribution Proposal Ready for Approval',
    message: 'MILP Engine formulated Transfer PRO-2026-088: 450 packs of Metformin 500mg from St. Paul Hospital to Hawassa Referral (Net ETB 42,500 saved).',
    severity: 'medium',
    timestamp: '3 hours ago',
    facility: 'St. Paul Hospital Millennium Medical College',
    category: 'Redistribution',
    isRead: false,
    actionUrl: '/redistribution'
  },
  {
    id: 'notif-4',
    title: 'Data Quality Anomaly Detected',
    message: 'Completeness check detected 4 missing consumption log entries during weekly batch synchronization for Felege Hiwot Hospital.',
    severity: 'medium',
    timestamp: '5 hours ago',
    facility: 'Felege Hiwot Comprehensive Specialized Hospital',
    category: 'Quality',
    isRead: true,
    actionUrl: '/data-quality'
  },
  {
    id: 'notif-5',
    title: 'AI Model Re-benchmarking Complete',
    message: 'Monthly automated Croston-TSB vs. LightGBM comparative evaluation finished. Ensemble model achieved 11.4% WAPE on intermittent demand patterns.',
    severity: 'info',
    timestamp: '1 day ago',
    facility: 'System-wide',
    category: 'Model',
    isRead: true,
    actionUrl: '/ai-laboratory'
  }
];

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<NotificationItem[]>(INITIAL_NOTIFICATIONS);
  const [filterSeverity, setFilterSeverity] = useState<string>('all');
  const [filterCategory, setFilterCategory] = useState<string>('all');

  const unreadCount = notifications.filter(n => !n.isRead).length;

  const handleMarkAsRead = (id: string) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, isRead: true } : n));
  };

  const handleMarkAllRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, isRead: true })));
  };

  const handleClearAll = () => {
    setNotifications([]);
  };

  const filteredNotifications = notifications.filter(n => {
    if (filterSeverity !== 'all' && n.severity !== filterSeverity) return false;
    if (filterCategory !== 'all' && n.category !== filterCategory) return false;
    return true;
  });

  const getSeverityBadge = (severity: NotificationItem['severity']) => {
    switch (severity) {
      case 'critical':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 border border-rose-200">
            <AlertCircle className="w-3 h-3 text-rose-600" /> Critical
          </span>
        );
      case 'high':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200">
            <AlertTriangle className="w-3 h-3 text-amber-600" /> High Risk
          </span>
        );
      case 'medium':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 border border-blue-200">
            <Info className="w-3 h-3 text-blue-600" /> Action Required
          </span>
        );
      case 'info':
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">
            <CheckCircle2 className="w-3 h-3 text-slate-500" /> Advisory
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">
      <DemoAlert 
        title="Live Alert Notification Feed"
        description="Simulated emergency inventory push notifications, automated SMS/email webhook dispatches, and FEFO expiry triggers for healthcare supply chain managers."
      />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">Alerts & Notifications</h1>
            {unreadCount > 0 && (
              <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-rose-600 text-white">
                {unreadCount} unread
              </span>
            )}
          </div>
          <p className="text-sm text-slate-500 mt-1">
            Real-time alert dispatch center for stockout warnings, FEFO expiry risks, and optimization proposals.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {unreadCount > 0 && (
            <button
              onClick={handleMarkAllRead}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-300 bg-white text-xs font-medium text-slate-700 hover:bg-slate-50 shadow-sm transition"
            >
              <Check className="w-3.5 h-3.5 text-slate-500" /> Mark all read
            </button>
          )}
          {notifications.length > 0 && (
            <button
              onClick={handleClearAll}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-300 bg-white text-xs font-medium text-rose-600 hover:bg-rose-50 shadow-sm transition"
            >
              <Trash2 className="w-3.5 h-3.5" /> Clear feed
            </button>
          )}
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Unread Alerts</span>
            <Bell className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-2">{unreadCount}</div>
          <div className="text-xs text-slate-500 mt-1">Pending review by logistics team</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Critical Emergencies</span>
            <ShieldAlert className="w-4 h-4 text-rose-600" />
          </div>
          <div className="text-2xl font-bold text-rose-600 mt-2">
            {notifications.filter(n => n.severity === 'critical').length}
          </div>
          <div className="text-xs text-rose-600 mt-1">Requires immediate manual action</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Dispatched Today</span>
            <Send className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-bold text-emerald-700 mt-2">34 SMS / Email</div>
          <div className="text-xs text-slate-500 mt-1">Sent to regional health bureaus</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase">
            <span>Channels Status</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-bold text-slate-900 mt-2">Active</div>
          <div className="text-xs text-emerald-600 mt-1">SMTP & SMS Webhooks connected</div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center gap-4">
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-600">
          <Filter className="w-4 h-4 text-slate-400" /> Filter:
        </div>
        <div>
          <select
            value={filterSeverity}
            onChange={(e) => setFilterSeverity(e.target.value)}
            className="text-xs border border-slate-300 rounded-lg px-2.5 py-1.5 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Severities</option>
            <option value="critical">Critical</option>
            <option value="high">High Risk</option>
            <option value="medium">Action Required</option>
            <option value="info">Advisory</option>
          </select>
        </div>
        <div>
          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="text-xs border border-slate-300 rounded-lg px-2.5 py-1.5 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Categories</option>
            <option value="Stockout">Stockout Alerts</option>
            <option value="Expiry">Expiry Warnings</option>
            <option value="Redistribution">Redistribution Proposals</option>
            <option value="Quality">Data Quality</option>
            <option value="Model">AI Models</option>
          </select>
        </div>
      </div>

      {/* Notifications List */}
      <div className="space-y-3">
        {filteredNotifications.length === 0 ? (
          <div className="p-12 text-center bg-white rounded-xl border border-slate-200">
            <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto mb-3" />
            <h3 className="text-base font-semibold text-slate-800">No alerts match your criteria</h3>
            <p className="text-xs text-slate-500 mt-1">All active alerts have been resolved or filtered out.</p>
          </div>
        ) : (
          filteredNotifications.map((notif) => (
            <div
              key={notif.id}
              className={`p-4 rounded-xl border transition flex flex-col md:flex-row md:items-center justify-between gap-4 ${
                notif.isRead 
                  ? 'bg-white border-slate-200 opacity-80' 
                  : 'bg-blue-50/40 border-blue-200 shadow-xs'
              }`}
            >
              <div className="space-y-1.5 max-w-3xl">
                <div className="flex flex-wrap items-center gap-2">
                  {getSeverityBadge(notif.severity)}
                  <span className="text-xs font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                    {notif.category}
                  </span>
                  <span className="text-xs text-slate-400">• {notif.timestamp}</span>
                  <span className="text-xs font-medium text-slate-600">• {notif.facility}</span>
                </div>
                <h4 className="text-sm font-semibold text-slate-900">{notif.title}</h4>
                <p className="text-xs text-slate-600 leading-relaxed">{notif.message}</p>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                {!notif.isRead && (
                  <button
                    onClick={() => handleMarkAsRead(notif.id)}
                    className="p-1.5 rounded-lg border border-slate-200 bg-white text-slate-600 hover:bg-slate-100 text-xs font-medium transition"
                    title="Mark as read"
                  >
                    <Check className="w-4 h-4 text-emerald-600" />
                  </button>
                )}
                {notif.actionUrl && (
                  <a
                    href={notif.actionUrl}
                    className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium shadow-xs transition"
                  >
                    Take Action <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
