'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { DemoAlert } from '@/components/ui/DemoAlert';
import { settingsApi } from '@/lib/api';
import { SystemSettings } from '@/types';
import {
  Settings,
  Save,
  RotateCcw,
  CheckCircle2,
  Sliders,
  Bell,
  Truck,
  Shield,
  Clock,
  Database,
  Radio,
} from 'lucide-react';

export default function SettingsPage() {
  const [settings, setSettings] = useState<SystemSettings>({
    auto_reorder_enabled: true,
    donor_safety_stock_buffer_days: 25,
    max_transfer_radius_km: 350,
    stockout_alert_threshold_dsr: 10,
    expiry_warning_threshold_days: 90,
    fefo_strict_mode: true,
    sms_alert_notifications: true,
    email_digest_frequency: 'Daily',
  });

  const [savedNotification, setSavedNotification] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    const loaded = settingsApi.get();
    setSettings(loaded);
  }, []);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setSavedNotification(null);
    try {
      const updated = settingsApi.update(settings);
      setSettings(updated);
      setSavedNotification('System configuration and MILP solver constraints saved successfully.');
    } catch (err: any) {
      alert(`Failed to save settings: ${err.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  const handleResetDefaults = () => {
    if (confirm('Reset all parameters to Ethiopian Ministry of Health default baseline?')) {
      const defaults: SystemSettings = {
        auto_reorder_enabled: true,
        donor_safety_stock_buffer_days: 25,
        max_transfer_radius_km: 350,
        stockout_alert_threshold_dsr: 10,
        expiry_warning_threshold_days: 90,
        fefo_strict_mode: true,
        sms_alert_notifications: true,
        email_digest_frequency: 'Daily',
      };
      const updated = settingsApi.update(defaults);
      setSettings(updated);
      setSavedNotification('All operational thresholds reset to MOH national defaults.');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            System Configuration &amp; Policy Settings
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Global constraints for MILP optimization solver, FEFO inventory queues, and alert thresholds.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleResetDefaults}>
            <RotateCcw className="w-3.5 h-3.5 mr-1.5" />
            Reset Defaults
          </Button>
          <Button variant="primary" size="sm" onClick={handleSave} isLoading={isSaving}>
            <Save className="w-3.5 h-3.5 mr-1.5" />
            Save Changes
          </Button>
        </div>
      </div>

      <DemoAlert
        title="Optimization Constraint Parameters"
        message="Settings directly dictate the mathematical bounds of the SCIP MILP engine and FEFO burn-down simulations across all regional facilities."
      />

      {savedNotification && (
        <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-2 shadow-2xs">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{savedNotification}</span>
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        {/* Section 1: Optimization & Redistribution Policy */}
        <Card
          title="MILP Lateral Redistribution Parameters"
          subtitle="Bounds governing mathematical transfer optimization between donor and recipient facilities"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
            <div className="space-y-1.5">
              <label className="font-semibold text-slate-800 block">
                Donor Safety Stock Buffer (Days)
              </label>
              <p className="text-slate-500 text-[11px] leading-relaxed">
                Minimum inventory buffer (in Days of Stock Remaining) that a donor hospital must retain. Transfers will never deplete below this threshold.
              </p>
              <input
                type="number"
                min="10"
                max="60"
                value={settings.donor_safety_stock_buffer_days}
                onChange={(e) =>
                  setSettings({ ...settings, donor_safety_stock_buffer_days: Number(e.target.value) })
                }
                className="w-full px-3 py-2 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white text-slate-900 font-bold"
              />
            </div>

            <div className="space-y-1.5">
              <label className="font-semibold text-slate-800 block">
                Maximum Lateral Transit Radius (Kilometers)
              </label>
              <p className="text-slate-500 text-[11px] leading-relaxed">
                Logistics distance limit calculated via Haversine great-circle route. Proposed routes exceeding this limit are pruned.
              </p>
              <input
                type="number"
                min="50"
                max="1000"
                step="25"
                value={settings.max_transfer_radius_km}
                onChange={(e) =>
                  setSettings({ ...settings, max_transfer_radius_km: Number(e.target.value) })
                }
                className="w-full px-3 py-2 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white text-slate-900 font-bold"
              />
            </div>

            <div className="space-y-2 md:col-span-2 pt-2 border-t border-slate-100">
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-semibold text-slate-800 block">
                    Automatic Lateral Transfer Proposals
                  </span>
                  <span className="text-slate-500 text-[11px]">
                    Periodically run SCIP solver to generate transfer recommendations whenever critical stockout or expiry deficits occur.
                  </span>
                </div>
                <input
                  type="checkbox"
                  checked={settings.auto_reorder_enabled}
                  onChange={(e) =>
                    setSettings({ ...settings, auto_reorder_enabled: e.target.checked })
                  }
                  className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
        </Card>

        {/* Section 2: FEFO & Stockout Alerts */}
        <Card
          title="Stockout & Expiry Warning Thresholds"
          subtitle="Define when critical and high-risk indicators are triggered on facility dashboards"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
            <div className="space-y-1.5">
              <label className="font-semibold text-slate-800 block">
                Critical Stockout Threshold (Days of Stock Remaining)
              </label>
              <p className="text-slate-500 text-[11px]">
                Items with DSR at or below this value are flagged as Critical Stockout Risks.
              </p>
              <input
                type="number"
                min="3"
                max="30"
                value={settings.stockout_alert_threshold_dsr}
                onChange={(e) =>
                  setSettings({ ...settings, stockout_alert_threshold_dsr: Number(e.target.value) })
                }
                className="w-full px-3 py-2 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white text-slate-900 font-bold"
              />
            </div>

            <div className="space-y-1.5">
              <label className="font-semibold text-slate-800 block">
                Expiry Monitoring Horizon (Days Until Expiry)
              </label>
              <p className="text-slate-500 text-[11px]">
                Batches entering this time window undergo burn-down FEFO simulation.
              </p>
              <input
                type="number"
                min="30"
                max="180"
                step="15"
                value={settings.expiry_warning_threshold_days}
                onChange={(e) =>
                  setSettings({ ...settings, expiry_warning_threshold_days: Number(e.target.value) })
                }
                className="w-full px-3 py-2 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white text-slate-900 font-bold"
              />
            </div>

            <div className="space-y-2 md:col-span-2 pt-2 border-t border-slate-100">
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-semibold text-slate-800 block">
                    Strict First-Expired, First-Out (FEFO) Enforcement
                  </span>
                  <span className="text-slate-500 text-[11px]">
                    Requires pharmacy dispensing staff to confirm earliest-expiring batch lot numbers prior to recording stock issues.
                  </span>
                </div>
                <input
                  type="checkbox"
                  checked={settings.fefo_strict_mode}
                  onChange={(e) =>
                    setSettings({ ...settings, fefo_strict_mode: e.target.checked })
                  }
                  className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
        </Card>

        {/* Section 3: Notification & Digest Frequency */}
        <Card
          title="Notification Dispatch Preferences"
          subtitle="Configure automated alert routing for regional pharmacists and clinical directors"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
            <div className="space-y-1.5">
              <label className="font-semibold text-slate-800 block">
                Executive Digest Frequency
              </label>
              <select
                value={settings.email_digest_frequency}
                onChange={(e) =>
                  setSettings({ ...settings, email_digest_frequency: e.target.value as any })
                }
                className="w-full px-3 py-2 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white text-slate-800 font-medium"
              >
                <option value="Daily">Daily Morning Summary (08:00 EAT)</option>
                <option value="Weekly">Weekly Monday Overview</option>
                <option value="Realtime">Realtime Instant Dispatch</option>
              </select>
            </div>

            <div className="space-y-2 pt-4">
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-semibold text-slate-800 block">
                    Emergency SMS Gateway Notifications
                  </span>
                  <span className="text-slate-500 text-[11px]">
                    Send critical alerts via Ethio Telecom SMS gateway for vital emergency medicine stockouts.
                  </span>
                </div>
                <input
                  type="checkbox"
                  checked={settings.sms_alert_notifications}
                  onChange={(e) =>
                    setSettings({ ...settings, sms_alert_notifications: e.target.checked })
                  }
                  className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
        </Card>

        {/* Save Button Bar */}
        <div className="flex items-center justify-end gap-3 pt-2">
          <Button variant="outline" size="sm" type="button" onClick={handleResetDefaults}>
            Reset Defaults
          </Button>
          <Button variant="primary" size="sm" type="submit" isLoading={isSaving}>
            <Save className="w-3.5 h-3.5 mr-1.5" />
            Save Configuration
          </Button>
        </div>
      </form>
    </div>
  );
}
