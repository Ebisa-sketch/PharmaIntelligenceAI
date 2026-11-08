import type { Metadata } from 'next';
import './globals.css';
import { AuthProvider } from '@/context/AuthContext';

export const metadata: Metadata = {
  title: 'PharmaIntelligence AI - Ethiopian Pharmaceutical Intelligence System',
  description: 'AI Decision-Support System for Stockout Risk, Expiry Prevention, and Inventory Redistribution in Ethiopian Healthcare Facilities',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased bg-slate-50 text-slate-900 font-sans">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
