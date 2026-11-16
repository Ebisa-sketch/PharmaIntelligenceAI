import React from 'react';
import { Sparkles } from 'lucide-react';

interface DemoAlertProps {
  title?: string;
  message?: string;
  description?: string;
  className?: string;
}

export function DemoAlert({
  title = 'Demonstration & Simulation Environment',
  message,
  description,
  className = '',
}: DemoAlertProps) {
  const displayMessage = description || message || 'Values displayed in this section are synthetic reference scenarios calibrated to Ethiopian Health Tier guidelines for validation purposes.';

  return (
    <div
      className={`flex items-start gap-3 p-3.5 rounded-xl border border-blue-200/80 bg-blue-50/60 text-slate-700 text-xs ${className}`}
      role="note"
    >
      <div className="w-5 h-5 rounded-md bg-blue-600/10 text-blue-700 flex items-center justify-center shrink-0 mt-0.5">
        <Sparkles className="w-3.5 h-3.5" />
      </div>
      <div>
        <span className="font-semibold text-blue-900 block">{title}</span>
        <span className="text-slate-600 leading-relaxed mt-0.5 block">{displayMessage}</span>
      </div>
    </div>
  );
}

export default DemoAlert;
