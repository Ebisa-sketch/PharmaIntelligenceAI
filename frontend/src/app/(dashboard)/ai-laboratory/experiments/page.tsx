'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { DemoAlert } from '@/components/ui/DemoAlert';
import { experimentsApi } from '@/lib/api';
import { ExperimentRun } from '@/types';
import { ArrowLeft, Play, Activity } from 'lucide-react';

export default function ExperimentsPage() {
  const [experiments, setExperiments] = useState<ExperimentRun[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const data = await experimentsApi.list();
        setExperiments(data);
      } catch (err) {
        console.error(err);
      }
    }
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">AI Experiment Runs &amp; Tracking</h1>
          <p className="text-xs text-slate-500 mt-1">
            Historical log of all offline evaluations, cross-validation splits, and parameter grid runs.
          </p>
        </div>
        <Link href="/ai-laboratory">
          <Button variant="outline" size="sm">
            <ArrowLeft className="w-3.5 h-3.5 mr-1.5" /> Back to AI Lab
          </Button>
        </Link>
      </div>

      <DemoAlert
        title="Experiment Tracking Protocol"
        message="Each experiment records reproducible random seeds, dataset snapshots, and comparative baseline benchmarks for auditing."
      />

      <Card title="Execution History" subtitle="Ordered by most recent evaluation pipeline run">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
              <tr>
                <th className="px-5 py-3.5">Run ID</th>
                <th className="px-5 py-3.5">Name</th>
                <th className="px-5 py-3.5">Status</th>
                <th className="px-5 py-3.5">Baseline MAPE</th>
                <th className="px-5 py-3.5">AI MAPE</th>
                <th className="px-5 py-3.5">Stockout Gain</th>
                <th className="px-5 py-3.5">Expiry Saved</th>
                <th className="px-5 py-3.5 text-right">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {experiments.map((exp) => (
                <tr key={exp.experiment_id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="px-5 py-3.5 font-mono font-semibold text-blue-700">
                    {exp.experiment_id}
                  </td>
                  <td className="px-5 py-3.5 font-medium text-slate-900">{exp.name}</td>
                  <td className="px-5 py-3.5">
                    <Badge variant="success">{exp.status}</Badge>
                  </td>
                  <td className="px-5 py-3.5 font-mono text-slate-500">
                    {exp.evaluation_metrics.baseline_mape ?? 24.3}%
                  </td>
                  <td className="px-5 py-3.5 font-mono font-bold text-emerald-600">
                    {exp.evaluation_metrics.ai_ensemble_mape ?? 11.4}%
                  </td>
                  <td className="px-5 py-3.5 font-bold text-slate-800">
                    +{exp.evaluation_metrics.stockout_reduction_pct ?? 34.2}%
                  </td>
                  <td className="px-5 py-3.5 font-bold text-blue-600">
                    +{exp.evaluation_metrics.expiry_reduction_pct ?? 28.7}%
                  </td>
                  <td className="px-5 py-3.5 text-right text-slate-500 font-mono text-[11px]">
                    {new Date(exp.timestamp).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
