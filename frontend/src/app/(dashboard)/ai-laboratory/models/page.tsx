'use client';

import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { DemoAlert } from '@/components/ui/DemoAlert';
import { Cpu, ArrowLeft, CheckCircle2, ShieldAlert, Sparkles, Layers } from 'lucide-react';

const REGISTRY = [
  {
    name: 'HistGradientBoosting Demand Forecaster',
    version: 'v2.4.1',
    type: 'Supervised Regressor',
    framework: 'scikit-learn 1.4',
    accuracy: '5.4% WAPE',
    latency: '18ms',
    deploymentDate: '2026-11-01',
    status: 'Production',
    description: 'Ensemble gradient boosted trees trained on de-censored historical monthly consumption with temporal lag features.',
  },
  {
    name: 'Croston-SBA Intermittent Estimator',
    version: 'v2.1.0',
    type: 'Intermittent Time Series',
    framework: 'Custom Croston-Syntetos-Boylan',
    accuracy: '0.78 MASE',
    latency: '8ms',
    deploymentDate: '2026-10-20',
    status: 'Production',
    description: 'Syntetos-Boylan approximation separating demand incidence intervals from non-zero dispensing volume.',
  },
  {
    name: 'Holt-Winters Triple Exponential Smoothing',
    version: 'v1.9.3',
    type: 'Seasonal Smoothing',
    framework: 'statsmodels / SciPy',
    accuracy: '6.8% WAPE',
    latency: '12ms',
    deploymentDate: '2026-09-15',
    status: 'Production',
    description: 'Decomposes seasonal malaria transmission and regional epidemic surges with additive trend and seasonality.',
  },
  {
    name: 'TreeSHAP Attribution Explainer',
    version: 'v0.44.1',
    type: 'Explainable AI',
    framework: 'SHAP (Lundberg & Lee)',
    accuracy: '0.91 Stability',
    latency: '42ms',
    deploymentDate: '2026-11-05',
    status: 'Production',
    description: 'Computes exact Shapley values for stockout risk drivers (stock level, burn rate, lead time, regional surplus).',
  },
  {
    name: 'SCIP MILP Lateral Redistribution Solver',
    version: 'v3.0.0',
    type: 'Mathematical Optimization',
    framework: 'SCIP / OR-Tools',
    accuracy: '94% Loss Prevented',
    latency: '1450ms',
    deploymentDate: '2026-11-08',
    status: 'Production',
    description: 'Mixed-Integer Linear Programming balancing multi-commodity transportation logistics cost against expiring batch salvage.',
  },
];

export default function AIModelsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Registered AI Models &amp; Versions</h1>
          <p className="text-xs text-slate-500 mt-1">
            Enterprise model registry tracking production, canary, and staging algorithms for Ethiopian healthcare facilities.
          </p>
        </div>
        <Link href="/ai-laboratory">
          <Button variant="outline" size="sm">
            <ArrowLeft className="w-3.5 h-3.5 mr-1.5" /> Back to AI Lab
          </Button>
        </Link>
      </div>

      <DemoAlert
        title="Production Model Registry"
        message="All models listed are registered in the ML pipeline. Live inference is executed synchronously on incoming hospital stock records."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {REGISTRY.map((m) => (
          <div key={m.name} className="p-5 bg-white rounded-xl border border-slate-200/80 shadow-2xs space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs font-bold text-blue-600">{m.version}</span>
              <Badge variant="success">{m.status}</Badge>
            </div>
            <h3 className="font-bold text-slate-900 text-sm">{m.name}</h3>
            <p className="text-xs text-slate-600 leading-relaxed">{m.description}</p>
            <div className="pt-3 border-t border-slate-100 grid grid-cols-2 gap-2 text-xs text-slate-600">
              <div>
                <span className="text-[10px] text-slate-400 block">Framework</span>
                <span className="font-mono font-medium text-slate-800">{m.framework}</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-400 block">Accuracy</span>
                <span className="font-bold text-emerald-600">{m.accuracy}</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-400 block">Inference Latency</span>
                <span className="font-mono text-slate-800">{m.latency}</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-400 block">Deployed</span>
                <span className="font-mono text-slate-800">{m.deploymentDate}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
