export default function ResetPasswordPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg border border-slate-100 p-8 space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-2xl font-bold text-slate-900">Set New Password</h1>
          <p className="text-sm text-slate-500">Choose a new password for your account</p>
        </div>
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">New Password</label>
            <input type="password" placeholder="••••••••" className="w-full px-3 py-2 border rounded-md border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Confirm New Password</label>
            <input type="password" placeholder="••••••••" className="w-full px-3 py-2 border rounded-md border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" />
          </div>
          <button type="submit" className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md text-sm transition-colors">
            Update Password
          </button>
        </form>
      </div>
    </div>
  );
}
