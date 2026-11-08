export default function ForgotPasswordPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg border border-slate-100 p-8 space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-2xl font-bold text-slate-900">Reset Password</h1>
          <p className="text-sm text-slate-500">Enter your email to receive recovery instructions</p>
        </div>
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Email address</label>
            <input type="email" placeholder="user@pharmaintelligence.ai" className="w-full px-3 py-2 border rounded-md border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" />
          </div>
          <button type="submit" className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md text-sm transition-colors">
            Send Reset Link
          </button>
        </form>
      </div>
    </div>
  );
}
