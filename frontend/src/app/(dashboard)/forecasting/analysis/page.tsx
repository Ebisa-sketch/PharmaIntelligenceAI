'use client';

import { useState } from 'react';
import { 
  TrendingUp, 
  BarChart2, 
  Activity, 
  Layers, 
  Info, 
  AlertCircle,
  HelpCircle,
  ChevronRight
} from 'lucide-react';
import DemoAlert from '@/components/ui/DemoAlert';

interface CategoryBreakdown {
  category: string;
  adiRange: string;
  cv2Range: string;
  recommendedModel: string;
  skuCount: number;
  percentage: number;
  description: string;
  color: string;
}

const CATEGORIES: CategoryBreakdown[] = [
  {
    category: 'Smooth Demand',
    adiRange: 'ADI < 1.32',
    cv2Range: 'CV² < 0.49',
    recommendedModel: 'LightGBM / Exponential Smoothing',
    skuCount: 42,
    percentage: 35,
    description: 'Regular, predictable replenishment patterns with low variability between order cycles.',
    color: 'emerald'
  },
  {
    category: 'Intermittent Demand',
    adiRange: 'ADI ≥ 1.32',
    cv2Range: 'CV² < 0.49',
    recommendedModel: 'Croston-TSB / Syntetos-Boylan',
    skuCount: 38,
    percentage: 32,
    description: 'Sporadic demand with numerous zero-consumption periods but relatively constant non-zero order quantities.',
    color: 'blue'
  },
  {
    category: 'Erratic Demand',
    adiRange: 'ADI < 1.32',
    cv2Range: 'CV² ≥ 0.49',
    recommendedModel: 'LightGBM / Random Forest',
    skuCount: 24,
    percentage: 20,
    description: 'Frequent orders with high volatility in order size, often driven by periodic clinic distributions.',
    color: 'amber'
  },
  {
    category: 'Lumpy Demand',
    adiRange: 'ADI ≥ 1.32',
    cv2Range: 'CV² ≥ 0.49',
    recommendedModel: 'Zero-Inflated Poisson / Neural Ensemble',
    skuCount: 16,
    percentage: 13,
    description: 'Both irregular order timing and large, unpredictable quantity spikes (most challenging to forecast).',
    color: 'rose'
  }
];

export default function ForecastingAnalysisPage() {
  const [selectedCategory, setSelectedCategory] = useState<CategoryBreakdown>(CATEGORIES[0]);

  return (
    <div className="space-y-6">
      <DemoAlert 
        title="Syntetos-Boylan Demand Classification Engine"
        description="Demand stream segmentation using Average Demand Interval (ADI = 1.32) and Squared Coefficient of Variation (CV² = 0.49) to automatically assign the optimal forecasting algorithm per medicine."
      />

      {/* Header */}
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Demand Stream & Seasonality Analysis</h1>
        <p className="text-sm text-slate-500 mt-1">
          Deep-dive classification into intermittent vs. erratic patterns for pharmaceutical supplies in Ethiopian healthcare facilities.
        </p>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase">Total Catalog SKUs</div>
          <div className="text-2xl font-bold text-slate-900 mt-2">120 Medicines</div>
          <div className="text-xs text-slate-500 mt-1">Across essential health packages</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase">Intermittent / Lumpy Share</div>
          <div className="text-2xl font-bold text-amber-600 mt-2">45% of SKUs</div>
          <div className="text-xs text-amber-700 mt-1">Requires Croston-TSB formulation</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase">Average WAPE (Ensemble)</div>
          <div className="text-2xl font-bold text-emerald-600 mt-2">11.8%</div>
          <div className="text-xs text-emerald-700 mt-1">Over 90-day test backtesting</div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold text-slate-500 uppercase">Seasonal Surge Factor</div>
          <div className="text-2xl font-bold text-blue-600 mt-2">+24.5%</div>
          <div className="text-xs text-blue-700 mt-1">Peak malaria season adjustment</div>
        </div>
      </div>

      {/* Syntetos-Boylan Matrix Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Categories List */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-slate-900">Syntetos-Boylan Quadrant Breakdown</h3>
            <span className="text-xs text-slate-500">120 SKUs Evaluated</span>
          </div>

          <div className="space-y-3">
            {CATEGORIES.map((cat) => (
              <div
                key={cat.category}
                onClick={() => setSelectedCategory(cat)}
                className={`p-4 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                  selectedCategory.category === cat.category
                    ? 'border-blue-500 bg-blue-50/50 shadow-xs'
                    : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-slate-900">{cat.category}</span>
                    <span className="text-[10px] font-mono text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
                      {cat.adiRange} | {cat.cv2Range}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500">{cat.recommendedModel}</p>
                </div>

                <div className="text-right">
                  <div className="text-sm font-bold text-slate-900">{cat.skuCount} SKUs</div>
                  <div className="text-xs text-slate-500">{cat.percentage}%</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Selected Category Details */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-5">
          <div className="flex items-center gap-2 border-b border-slate-200 pb-3">
            <Layers className="w-5 h-5 text-blue-600" />
            <h3 className="text-base font-semibold text-slate-900">{selectedCategory.category} Profile</h3>
          </div>

          <p className="text-xs text-slate-600 leading-relaxed">
            {selectedCategory.description}
          </p>

          <div className="space-y-3">
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <div className="text-[11px] font-semibold text-slate-500 uppercase">Recommended Model Pipeline</div>
              <div className="text-xs font-bold text-slate-900 mt-1">{selectedCategory.recommendedModel}</div>
            </div>

            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <div className="text-[11px] font-semibold text-slate-500 uppercase">Cutoff Criteria</div>
              <div className="text-xs font-mono text-slate-800 mt-1">
                Average Demand Interval: {selectedCategory.adiRange} <br />
                Squared Coeff. of Variation: {selectedCategory.cv2Range}
              </div>
            </div>

            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <div className="text-[11px] font-semibold text-slate-500 uppercase">Sample Representative Medicines</div>
              <ul className="text-xs text-slate-700 mt-1.5 list-disc pl-4 space-y-0.5">
                {selectedCategory.category === 'Smooth Demand' && (
                  <>
                    <li>Amoxicillin 500mg Capsule (Daily constant throughput)</li>
                    <li>Paracetamol 500mg Tablet (High frequency baseline)</li>
                  </>
                )}
                {selectedCategory.category === 'Intermittent Demand' && (
                  <>
                    <li>Artemether-Lumefantrine 20/120mg (High seasonality pulses)</li>
                    <li>Ceftriaxone 1g Injection (Inpatient specialty surges)</li>
                  </>
                )}
                {selectedCategory.category === 'Erratic Demand' && (
                  <>
                    <li>Oxytocin 10 IU/ml (Variable clinic replenishment bulk)</li>
                    <li>Ringer Lactate 500ml IV Infusion (Surge trauma demands)</li>
                  </>
                )}
                {selectedCategory.category === 'Lumpy Demand' && (
                  <>
                    <li>Rabies Vaccine 2.5 IU (Rare, clustered bite emergencies)</li>
                    <li>Snake Antivenom Polyclonal (Sporadic high volume incidents)</li>
                  </>
                )}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Stockout De-censoring Investigation (README Section 10.2 & Research Question RQ2) */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border-b border-slate-200 pb-3">
          <div>
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-indigo-600" />
              <h3 className="text-base font-bold text-slate-900">Stockout De-censoring Investigation (RQ2 / Section 10.2)</h3>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Distinguishing True Zero Consumption from Censored Zeroes to Prevent Downward Demand Bias
            </p>
          </div>
          <span className="text-[11px] font-semibold bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded-full border border-indigo-200 self-start sm:self-auto">
            Transformer: RULE-C01 &amp; C02 Active
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span className="text-[11px] font-bold uppercase text-slate-500">The Stockout-Censoring Problem</span>
            <p className="text-xs text-slate-600 leading-relaxed">
              When a healthcare facility runs out of stock, recorded patient issues drop to zero. A naive ML algorithm interprets this as zero patient demand, forecasting lower replenishment orders and trapping the hospital in a perpetual stockout spiral.
            </p>
          </div>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span className="text-[11px] font-bold uppercase text-slate-500">Mathematical De-censoring Formulation</span>
            <div className="text-xs font-mono text-slate-800 space-y-1 bg-white p-2.5 rounded border border-slate-200">
              <div>R = (T - S) / T &nbsp;&nbsp;[In-Stock Ratio]</div>
              <div>If 0.10 ≤ R &lt; 0.90:</div>
              <div className="text-indigo-700 font-bold">y_adj = y_obs / R</div>
              <div>If R &lt; 0.10: Impute rolling median</div>
            </div>
          </div>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span className="text-[11px] font-bold uppercase text-slate-500">True Zero vs. Censored Zero</span>
            <div className="text-xs text-slate-600 space-y-1.5">
              <div className="flex items-start gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-500 mt-1 shrink-0"></span>
                <span><strong>True Zero:</strong> Closing stock &gt; 0, consumption = 0. No adjustment needed (genuine absence of morbidity).</span>
              </div>
              <div className="flex items-start gap-1.5">
                <span className="w-2 h-2 rounded-full bg-rose-500 mt-1 shrink-0"></span>
                <span><strong>Censored Zero:</strong> Closing stock = 0, stockout days = 30. Imputed using in-stock periods.</span>
              </div>
            </div>
          </div>
        </div>

        {/* Empirical De-censoring Series Sample */}
        <div className="border border-slate-200 rounded-lg overflow-hidden">
          <div className="px-4 py-2.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-700">
              Empirical Transformation Sample: Amoxicillin 500mg (12-Month Ingestion Log)
            </span>
            <span className="text-[10px] text-slate-500">Units: Blister Packs</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-100/70 text-[10px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                <tr>
                  <th className="px-4 py-2">Month</th>
                  <th className="px-4 py-2">Observed Issues (y_obs)</th>
                  <th className="px-4 py-2">Stockout Days (S)</th>
                  <th className="px-4 py-2">In-Stock Ratio (R)</th>
                  <th className="px-4 py-2">De-censored Demand (y_adj)</th>
                  <th className="px-4 py-2">Classification</th>
                  <th className="px-4 py-2">Bias Correction</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-mono">
                <tr className="hover:bg-slate-50">
                  <td className="px-4 py-2 text-slate-900 font-medium">Month 1</td>
                  <td className="px-4 py-2">420</td>
                  <td className="px-4 py-2 text-emerald-600">0 days</td>
                  <td className="px-4 py-2">1.00</td>
                  <td className="px-4 py-2 font-bold text-slate-900">420.0</td>
                  <td className="px-4 py-2"><span className="text-[10px] font-sans px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 font-medium">UNCENSORED</span></td>
                  <td className="px-4 py-2 text-slate-500 font-sans">None (Full In-Stock)</td>
                </tr>
                <tr className="hover:bg-slate-50 bg-amber-50/30">
                  <td className="px-4 py-2 text-slate-900 font-medium">Month 2</td>
                  <td className="px-4 py-2 text-amber-700 font-bold">280</td>
                  <td className="px-4 py-2 text-amber-600 font-bold">10 days</td>
                  <td className="px-4 py-2 font-bold text-amber-700">0.67</td>
                  <td className="px-4 py-2 font-bold text-indigo-700">417.9</td>
                  <td className="px-4 py-2"><span className="text-[10px] font-sans px-1.5 py-0.5 rounded bg-amber-100 text-amber-800 font-medium">ADJUSTED</span></td>
                  <td className="px-4 py-2 text-emerald-700 font-sans font-medium">+137.9 units rescued</td>
                </tr>
                <tr className="hover:bg-slate-50 bg-rose-50/30">
                  <td className="px-4 py-2 text-slate-900 font-medium">Month 3</td>
                  <td className="px-4 py-2 text-rose-700 font-bold">0</td>
                  <td className="px-4 py-2 text-rose-600 font-bold">30 days</td>
                  <td className="px-4 py-2 font-bold text-rose-700">0.00</td>
                  <td className="px-4 py-2 font-bold text-indigo-700">420.0</td>
                  <td className="px-4 py-2"><span className="text-[10px] font-sans px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-medium">CENSORED_ZERO</span></td>
                  <td className="px-4 py-2 text-emerald-700 font-sans font-medium">+420.0 imputed (rolling median)</td>
                </tr>
                <tr className="hover:bg-slate-50">
                  <td className="px-4 py-2 text-slate-900 font-medium">Month 4</td>
                  <td className="px-4 py-2">435</td>
                  <td className="px-4 py-2 text-emerald-600">0 days</td>
                  <td className="px-4 py-2">1.00</td>
                  <td className="px-4 py-2 font-bold text-slate-900">435.0</td>
                  <td className="px-4 py-2"><span className="text-[10px] font-sans px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 font-medium">UNCENSORED</span></td>
                  <td className="px-4 py-2 text-slate-500 font-sans">None (Full In-Stock)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
