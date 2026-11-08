import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'PharmaIntelligence AI - Pharmaceutical Supply Chain Intelligence',
  description: 'AI-driven Pharmaceutical Supply Chain Intelligence & Demand Forecasting System',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased bg-slate-50 text-slate-900">
        {children}
      </body>
    </html>
  );
}
