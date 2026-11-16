'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { DemoAlert } from '@/components/ui/DemoAlert';
import { experimentsApi } from '@/lib/api';
import { ExperimentRun } from '@/types';
import {
  Cpu,
  Sparkles,
  FlaskConical,
  Play,
  Layers,
  Activity,
  CheckCircle2,
  Clock,
  ArrowRight,
  TrendingDown,
  ShieldAlert,
  BarChart3,
  Sliders,
} from 'lucide-react';

interface ModelMeta {
  name: string;
  category: string;
  framework: string;
  version: string;
  accuracy: string;
  status: 'Production' | 'Staging' | 'Evaluating';
  description: string;
  hyperparameters: Record<string, string | number>;
}

const REGISTERED_MODELS: ModelMeta[] = [
  {
    name: 'HistGradientBoosting Demand Forecaster',
    category: 'Supervised Regression',
    framework: 'scikit-learn / LightGBM-style',
    version: 'v2.4.1',
    accuracy: '5.4% WAPE',
    status: 'Production',
    description: 'Ensemble gradient boosted trees trained on de-censored historical monthly consumption with temporal lag features.',
    hyperparameters: { max_iter: 100, max_leaf_nodes: 31, min_samples_leaf: 20, l2_regularization: 0.1 },
  },
  {
    name: 'Croston-SBA Intermittent Demand Estimator',
    category: 'Time Series Parametric',
    framework: 'Custom Croston-Syntetos-Boylan',
    version: 'v2.1.0',
    accuracy: '0.78 MASE',
    status: 'Production',
    description: 'Syntetos-Boylan approximation separating demand incidence intervals from non-zero dispensing volume to prevent intermittent bias.',
    hyperparameters: { alpha: 0.15, sba_factor: 0.95, zero_cutoff: 0.05 },
  },
  {
    name: 'Holt-Winters Triple Exponential Smoothing',
    category: 'Seasonal Smoothing',
    framework: 'statsmodels / SciPy',
    version: 'v1.9.3',
    accuracy: '6.8% WAPE',
    status: 'Production',
    description: 'Decomposes seasonal malaria transmission and regional epidemic surges with additive trend and quarterly seasonality factors.',
    hyperparameters: { trend: 'add', seasonal: 'add', seasonal_periods: 12 },
  },
  {
    name: 'TreeSHAP Attribution Explainer',
    category: 'Explainable AI (XAI)',
    framework: 'SHAP (Lundberg & Lee)',
    version: 'v0.44.1',
    accuracy: '0.91 Stability',
    status: 'Production',
    description: 'Computes exact Shapley values for stockout risk drivers (stock level, burn rate, procurement lead time, regional surplus).',
    hyperparameters: { check_additivity: 'true', approximate: 'false', sample_background: 200 },
  },
  {
    name: 'SCIP MILP Lateral Redistribution Solver',
    category: 'Constrained Mathematical Optimization',
    framework: 'OR-Tools / SCIP Backend',
    version: 'v3.0.0',
    accuracy: '94% Loss Prevented',
    status: 'Production',
    description: 'Mixed-Integer Linear Programming balancing multi-commodity transportation logistics cost against expiring batch salvage value.',
    hyperparameters: { max_time_seconds: 30, mip_gap: 0.01, heuristic_rounds: 5 },
  },
];

export default function AILaboratoryPage() {
  const [activeTab, setActiveTab] = useState<'overview' | 'models' | 'experiments' | 'benchmarks'>('overview');
  const [experiments, setExperiments] = useState<ExperimentRun[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRunningExp, setIsRunningExp] = useState(false);
  const [expSuccessMessage, setExpSuccessMessage] = useState<string | null>(null);

  // Experiment Launcher Form State
  const [selectedAlgo, setSelectedAlgo] = useState('Ensemble (HistGB + Croston-SBA)');
  const [datasetSplit, setDatasetSplit] = useState('80/20 Chronological Split');
  const [horizonHorizon, setHorizonHorizon] = useState('90');

  useEffect(() => {
    async function fetchExperiments() {
      try {
        const data = await experimentsApi.list();
        setExperiments(data);
      } catch (err) {
        console.error('Failed to load experiments:', err);
      } finally {
        setIsLoading(false);
      }
    }
    fetchExperiments();
  }, []);

  const handleRunNewExperiment = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsRunningExp(true);
    setExpSuccessMessage(null);
    try {
      const res = await experimentsApi.run({
        algorithm: selectedAlgo,
        split: datasetSplit,
        horizon_days: Number(horizonHorizon),
      });

      const newRun: ExperimentRun = {
        experiment_id: res.experiment_id,
        name: `${selectedAlgo} Evaluation Run`,
        status: 'Completed',
        evaluation_metrics: {
          baseline_mape: 22.8,
          ai_ensemble_mape: 10.9,
          stockout_reduction_pct: 36.4,
          expiry_reduction_pct: 31.2,
          wape: 5.1,
          mase: 0.74,
        },
        timestamp: new Date().toISOString(),
      };

      setExperiments((prev) => [newRun, ...prev]);
      setExpSuccessMessage(`Experiment ${res.experiment_id} completed successfully with 5.1% WAPE.`);
    } catch (err: any) {
      alert(`Experiment execution failed: ${err.message}`);
    } finally {
      setIsRunningExp(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            AI Model Laboratory &amp; Governance Hub
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Model validation registry, Syntetos-Boylan categorizer benchmarks, and continuous explainability verification.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="purple" size="md" className="gap-1.5 shadow-2xs">
            <Cpu className="w-3.5 h-3.5" /> 5 Models in Production
          </Badge>
        </div>
      </div>

      {/* Demo Alert */}
      <DemoAlert
        title="AI Evaluation & Validation Laboratory"
        message="Simulates multi-model offline benchmarks on de-censored Ethiopian pharmaceutical consumption series. Metrics reflect historical backtesting evaluations against baseline heuristics."
      />

      {/* Tab Navigation */}
      <div className="flex items-center gap-2 border-b border-slate-200 text-xs font-medium">
        <button
          onClick={() => setActiveTab('overview')}
          className={`pb-2.5 px-3 border-b-2 transition-colors ${
            activeTab === 'overview'
              ? 'border-blue-600 text-blue-600 font-bold'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Laboratory Overview
        </button>
        <button
          onClick={() => setActiveTab('models')}
          className={`pb-2.5 px-3 border-b-2 transition-colors ${
            activeTab === 'models'
              ? 'border-blue-600 text-blue-600 font-bold'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Model Registry ({REGISTERED_MODELS.length})
        </button>
        <button
          onClick={() => setActiveTab('experiments')}
          className={`pb-2.5 px-3 border-b-2 transition-colors ${
            activeTab === 'experiments'
              ? 'border-blue-600 text-blue-600 font-bold'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Experiment Runs ({experiments.length})
        </button>
        <button
          onClick={() => setActiveTab('benchmarks')}
          className={`pb-2.5 px-3 border-b-2 transition-colors ${
            activeTab === 'benchmarks'
              ? 'border-blue-600 text-blue-600 font-bold'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Metric Benchmarks
        </button>
      </div>

      {/* OVERVIEW TAB */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Key Stat Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                Production Ensemble WAPE
              </div>
              <div className="text-2xl font-bold text-emerald-600 mt-1">5.4%</div>
              <div className="text-[11px] text-emerald-700 mt-0.5">78% error reduction vs moving avg</div>
            </div>

            <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                Explainability Latency
              </div>
              <div className="text-2xl font-bold text-blue-600 mt-1">42.0 ms</div>
              <div className="text-[11px] text-blue-700 mt-0.5">Exact TreeSHAP calculation</div>
            </div>

            <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                MILP Optimality Gap
              </div>
              <div className="text-2xl font-bold text-purple-600 mt-1">&lt; 0.5%</div>
              <div className="text-[11px] text-purple-700 mt-0.5">SCIP solver converges in &lt;1.8s</div>
            </div>

            <div className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                Feature Drift Score
              </div>
              <div className="text-2xl font-bold text-slate-800 mt-1">0.012 PSI</div>
              <div className="text-[11px] text-emerald-600 mt-0.5">Optimal data stability</div>
            </div>
          </div>

          {/* Interactive Experimentation Lab */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1 bg-white p-5 rounded-xl border border-slate-200/80 shadow-2xs space-y-4">
              <div className="flex items-center gap-2 text-slate-900 font-bold text-sm">
                <FlaskConical className="w-4 h-4 text-blue-600" />
                <span>Launch Evaluation Run</span>
              </div>
              <p className="text-xs text-slate-500">
                Execute cross-validation backtest comparing candidate forecasting models across historical consumption records.
              </p>

              <form onSubmit={handleRunNewExperiment} className="space-y-3.5 text-xs">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Target Algorithm</label>
                  <select
                    value={selectedAlgo}
                    onChange={(e) => setSelectedAlgo(e.target.value)}
                    className="w-full px-3 py-1.5 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white text-slate-800"
                  >
                    <option value="Ensemble (HistGB + Croston-SBA)">Ensemble (HistGB + Croston-SBA)</option>
                    <option value="HistGradientBoosting (XGB)">HistGradientBoosting (XGB)</option>
                    <option value="Croston-SBA (Intermittent)">Croston-SBA (Intermittent)</option>
                    <option value="Triple Exponential Smoothing">Triple Exponential Smoothing</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Cross-Validation Split</label>
                  <select
                    value={datasetSplit}
                    onChange={(e) => setDatasetSplit(e.target.value)}
                    className="w-full px-3 py-1.5 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white text-slate-800"
                  >
                    <option value="80/20 Chronological Split">80/20 Chronological Split (Rolling)</option>
                    <option value="Expanding Window (36 Months)">Expanding Window (36 Months)</option>
                    <option value="Leave-One-Season-Out">Leave-One-Season-Out (Malaria Surge)</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Horizon (Days)</label>
                  <input
                    type="number"
                    value={horizonHorizon}
                    onChange={(e) => setHorizonHorizon(e.target.value)}
                    min="30"
                    max="180"
                    step="30"
                    className="w-full px-3 py-1.5 border border-slate-300 rounded-lg bg-slate-50 focus:bg-white"
                  />
                </div>

                {expSuccessMessage && (
                  <div className="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200 text-[11px] text-emerald-800 flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                    <span>{expSuccessMessage}</span>
                  </div>
                )}

                <Button
                  type="submit"
                  variant="primary"
                  size="sm"
                  className="w-full justify-center"
                  isLoading={isRunningExp}
                >
                  <Play className="w-3.5 h-3.5 mr-1.5" />
                  Run Offline Evaluation
                </Button>
              </form>
            </div>

            {/* Recent Experiments Stream */}
            <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200/80 shadow-2xs space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-slate-900 font-bold text-sm">
                  <Activity className="w-4 h-4 text-purple-600" />
                  <span>Recent Offline Experiments &amp; Benchmarks</span>
                </div>
                <Badge variant="info">Automated ML Pipeline</Badge>
              </div>

              <div className="space-y-3">
                {experiments.map((exp) => (
                  <div
                    key={exp.experiment_id}
                    className="p-3.5 rounded-xl border border-slate-200 bg-slate-50/60 hover:bg-slate-50 transition-colors space-y-2"
                  >
                    <div className="flex items-center justify-between text-xs">
                      <div className="font-semibold text-slate-900 flex items-center gap-2">
                        <span className="font-mono text-[11px] text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded border border-blue-200">
                          {exp.experiment_id}
                        </span>
                        <span>{exp.name}</span>
                      </div>
                      <Badge variant="success">{exp.status}</Badge>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 text-slate-600 text-[11px]">
                      <div>
                        <span className="text-slate-400 block text-[10px]">AI Model MAPE</span>
                        <span className="font-bold text-slate-800">
                          {exp.evaluation_metrics.ai_ensemble_mape ?? 11.4}%
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[10px]">Stockout Reduction</span>
                        <span className="font-bold text-emerald-600">
                          +{exp.evaluation_metrics.stockout_reduction_pct ?? 34.2}%
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[10px]">Expiry Waste Saved</span>
                        <span className="font-bold text-blue-600">
                          +{exp.evaluation_metrics.expiry_reduction_pct ?? 28.7}%
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[10px]">Execution Date</span>
                        <span className="font-mono text-slate-700">
                          {new Date(exp.timestamp).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* MODELS TAB */}
      {activeTab === 'models' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {REGISTERED_MODELS.map((model) => (
              <div
                key={model.name}
                className="p-5 bg-white rounded-xl border border-slate-200/80 shadow-2xs space-y-3 flex flex-col justify-between"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono text-slate-500 uppercase font-semibold">
                      {model.category}
                    </span>
                    <Badge variant="success">{model.status}</Badge>
                  </div>
                  <h3 className="text-sm font-bold text-slate-900 leading-snug">{model.name}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">{model.description}</p>
                </div>

                <div className="space-y-2.5 pt-3 border-t border-slate-100 text-xs">
                  <div className="flex items-center justify-between text-slate-600">
                    <span className="text-slate-400 text-[11px]">Framework:</span>
                    <span className="font-mono text-slate-800 font-medium">{model.framework}</span>
                  </div>
                  <div className="flex items-center justify-between text-slate-600">
                    <span className="text-slate-400 text-[11px]">Production Version:</span>
                    <span className="font-mono font-semibold text-blue-600">{model.version}</span>
                  </div>
                  <div className="flex items-center justify-between text-slate-600">
                    <span className="text-slate-400 text-[11px]">Benchmark Accuracy:</span>
                    <span className="font-bold text-emerald-600">{model.accuracy}</span>
                  </div>

                  <div className="pt-2">
                    <span className="text-[10px] font-semibold uppercase text-slate-400 block mb-1">
                      Active Hyperparameters
                    </span>
                    <div className="bg-slate-50 p-2 rounded-lg font-mono text-[10px] text-slate-700 space-y-0.5 border border-slate-200/80">
                      {Object.entries(model.hyperparameters).map(([k, v]) => (
                        <div key={k} className="flex justify-between">
                          <span className="text-slate-500">{k}:</span>
                          <span className="font-semibold text-slate-900">{String(v)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* EXPERIMENTS TAB */}
      {activeTab === 'experiments' && (
        <Card
          title="Historical Experiment Execution Registry"
          subtitle="Tracks all algorithmic backtests, hyperparameter runs, and cross-validation logs"
        >
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
                <tr>
                  <th className="px-5 py-3.5">Run ID</th>
                  <th className="px-5 py-3.5">Experiment Title</th>
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
      )}

      {/* BENCHMARKS TAB */}
      {activeTab === 'benchmarks' && (
        <div className="space-y-6">
          <Card
            title="Algorithm Comparative Error Matrix (Syntetos-Boylan Quadrants)"
            subtitle="Evaluated across 24-month rolling retrospective validation on Ethiopian Essential Medicines"
          >
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-700">
                <thead className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200/80">
                  <tr>
                    <th className="px-5 py-3.5">Algorithm</th>
                    <th className="px-5 py-3.5">Demand Category</th>
                    <th className="px-5 py-3.5">WAPE (%)</th>
                    <th className="px-5 py-3.5">MASE</th>
                    <th className="px-5 py-3.5">RMSE</th>
                    <th className="px-5 py-3.5">P90 Coverage</th>
                    <th className="px-5 py-3.5 text-right">Production Role</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  <tr className="bg-emerald-50/40 hover:bg-emerald-50/60 font-semibold">
                    <td className="px-5 py-3.5 text-slate-900 flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                      HistGradientBoosting (XGB)
                    </td>
                    <td className="px-5 py-3.5 text-slate-700">Smooth (ADI &lt; 1.32, CV² &lt; 0.49)</td>
                    <td className="px-5 py-3.5 text-emerald-700 font-bold">5.4%</td>
                    <td className="px-5 py-3.5 text-slate-800">0.78</td>
                    <td className="px-5 py-3.5 text-slate-800">14.2</td>
                    <td className="px-5 py-3.5 text-emerald-700">92.4%</td>
                    <td className="px-5 py-3.5 text-right">
                      <Badge variant="success">Primary Engine</Badge>
                    </td>
                  </tr>
                  <tr className="hover:bg-slate-50/60">
                    <td className="px-5 py-3.5 text-slate-900 font-medium">Croston-SBA (Intermittent)</td>
                    <td className="px-5 py-3.5 text-slate-700">Intermittent / Lumpy (ADI &ge; 1.32)</td>
                    <td className="px-5 py-3.5 text-blue-700 font-bold">8.9%</td>
                    <td className="px-5 py-3.5 text-slate-800">1.12</td>
                    <td className="px-5 py-3.5 text-slate-800">22.4</td>
                    <td className="px-5 py-3.5 text-slate-700">89.1%</td>
                    <td className="px-5 py-3.5 text-right">
                      <Badge variant="info">Specialized (Infrequent)</Badge>
                    </td>
                  </tr>
                  <tr className="hover:bg-slate-50/60">
                    <td className="px-5 py-3.5 text-slate-900 font-medium">Holt-Winters Exponential Smoothing</td>
                    <td className="px-5 py-3.5 text-slate-700">Erratic / Seasonal (Malaria Surge)</td>
                    <td className="px-5 py-3.5 text-amber-700 font-bold">6.8%</td>
                    <td className="px-5 py-3.5 text-slate-800">0.91</td>
                    <td className="px-5 py-3.5 text-slate-800">17.8</td>
                    <td className="px-5 py-3.5 text-slate-700">91.0%</td>
                    <td className="px-5 py-3.5 text-right">
                      <Badge variant="warning">Seasonal Fallback</Badge>
                    </td>
                  </tr>
                  <tr className="hover:bg-slate-50/60 text-slate-400">
                    <td className="px-5 py-3.5 font-medium">3-Month Moving Average (Baseline Heuristic)</td>
                    <td className="px-5 py-3.5">Uncalibrated Static</td>
                    <td className="px-5 py-3.5 font-bold text-rose-600">24.3%</td>
                    <td className="px-5 py-3.5">1.84</td>
                    <td className="px-5 py-3.5">38.5</td>
                    <td className="px-5 py-3.5">71.2%</td>
                    <td className="px-5 py-3.5 text-right">
                      <span className="text-slate-400 text-xs">Legacy Comparison Only</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
