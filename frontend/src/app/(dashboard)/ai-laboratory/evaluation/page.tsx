'use client';

import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { DemoAlert } from '@/components/ui/DemoAlert';
import { ArrowLeft, CheckCircle2, TrendingUp, Sparkles } from 'lucide-react';

export default function EvaluationPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Model Evaluation Metrics</h1>
          <p className="text-xs text-slate-500 mt-1">
            Comparative accuracy evaluation across intermittent, smooth, and seasonal pharmaceutical demand patterns.
          </p>
        </div>
        <Link href="/ai-laboratory">
          <Button variant="outline" size="sm">
            <ArrowLeft className="w-3.5 h-3.5 mr-1.5" /> Back to AI Lab
          </Button>
        </Link>
      </div>

      <DemoAlert
        title="Evaluation Methodology"
        message="Metrics evaluated on 10,000+ simulated hospital dispensing transactions de-censored for historical stockout zeroes."
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">WAPE Across All Tiers</div>
          <div className="text-2xl font-bold text-emerald-600 mt-1">5.4%</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Weighted Absolute Percentage Error</div>
        </div>
        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">MASE Scaled Error</div>
          <div className="text-2xl font-bold text-blue-600 mt-1">0.78</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Superior to naive random walk (&lt;1.0)</div>
        </div>
        <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Coverage Rate (P10 - P90)</div>
          <div className="text-2xl font-bold text-purple-600 mt-1">92.4%</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Confidence interval calibration score</div>
        </div>
      </div>
    </div>
  );
}
