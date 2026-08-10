import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const navItems = [
  { to: "/app/dashboard", label: "🏠 Dashboard" },
  { to: "/app/tickets", label: "🎫 Tickets" },
  { to: "/app/create-ticket", label: "➕ New Ticket" },
  { to: "/app/documents", label: "📄 Documents" },
  { to: "/app/upload", label: "⬆️ Upload" },
  { to: "/app/users", label: "👥 Users", adminOnly: true },
  { to: "/app/profile", label: "⚙️ Profile" },
];

export default function ProtectedLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="mx-auto flex min-h-screen max-w-7xl">
        <aside className="hidden w-72 shrink-0 flex-col border-r border-slate-200 bg-slate-50 p-6 lg:flex">
          <div className="mb-10">
            <p className="text-sm uppercase tracking-[0.28em] text-slate-500">Enterprise AI</p>
            <h1 className="mt-4 text-2xl font-semibold text-slate-900">Ticket Resolution</h1>
          </div>

          <nav className="space-y-2">
            {navItems.map((item) => {
              if (item.adminOnly && user?.role !== "admin") {
                return null;
              }
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `block rounded-2xl px-4 py-3 text-sm font-medium transition ${
                      isActive ? "bg-indigo-600 text-white" : "text-slate-700 hover:bg-slate-100"
                    }`
                  }
                >
                  {item.label}
                </NavLink>
              );
            })}
          </nav>

          <div className="mt-auto space-y-2 pt-8">
            <div className="rounded-2xl bg-slate-100 p-4 text-sm text-slate-700">
              <p className="font-semibold">Signed in as</p>
              <p className="mt-2">{user?.full_name}</p>
              <p className="text-slate-500">{user?.role}</p>
            </div>
            <button
              type="button"
              onClick={handleLogout}
              className="w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-left text-sm font-medium text-slate-700 transition hover:bg-slate-50"
            >
              🚪 Logout
            </button>
          </div>
        </aside>

        <main className="flex-1 p-6 lg:px-10 lg:py-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
