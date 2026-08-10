import { useAuth } from "../context/AuthContext";

export default function ProfilePage() {
  const { user } = useAuth();

  return (
    <div className="rounded-3xl bg-white p-8 shadow-sm">
      <h1 className="text-3xl font-semibold text-slate-900">Profile</h1>
      <p className="mt-2 text-slate-500">Your account details and role information.</p>

      <div className="mt-8 grid gap-6 md:grid-cols-2">
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <h2 className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Full name</h2>
          <p className="mt-3 text-lg text-slate-900">{user?.full_name || "—"}</p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <h2 className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Email</h2>
          <p className="mt-3 text-lg text-slate-900">{user?.email || "—"}</p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <h2 className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Role</h2>
          <p className="mt-3 text-lg text-slate-900">{user?.role || "—"}</p>
        </div>
      </div>
    </div>
  );
}
