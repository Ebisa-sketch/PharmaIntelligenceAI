import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8 bg-gradient-to-b from-slate-50 to-slate-100">
      <div className="max-w-3xl text-center space-y-6">
        <div className="inline-block px-4 py-1.5 rounded-full bg-blue-100 text-blue-700 text-sm font-semibold tracking-wide">
          Next-Gen Healthcare Analytics
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 tracking-tight">
          PharmaIntelligence AI
        </h1>
        <p className="text-lg md:text-xl text-slate-600 max-w-2xl mx-auto">
          AI-Powered Pharmaceutical Supply Chain Intelligence, Demand Forecasting, Stockout Prevention, and Inventory Optimization.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            href="/dashboard"
            className="px-6 py-3 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium shadow-md transition-colors"
          >
            Launch Dashboard
          </Link>
          <Link
            href="/login"
            className="px-6 py-3 rounded-lg border border-slate-300 hover:bg-slate-200 text-slate-700 font-medium transition-colors"
          >
            Sign In
          </Link>
        </div>
      </div>
    </main>
  );
}
