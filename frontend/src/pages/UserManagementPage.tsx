import { useEffect, useState } from "react";
import { fetchUsers } from "../services/users";
import type { User } from "../types";

export default function UserManagementPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUsers()
      .then((data) => setUsers(data))
      .catch(() => setError("Unable to load users."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">User management</h1>
          <p className="text-slate-500">Admin-only access to user accounts.</p>
        </div>
      </div>

      <div className="rounded-2xl bg-white p-6 shadow-sm">
        {loading ? (
          <p className="text-slate-500">Loading users...</p>
        ) : error ? (
          <p className="text-red-600">{error}</p>
        ) : (
          <div className="grid gap-4">
            {users.map((user) => (
              <div key={user.id} className="rounded-xl border p-4">
                <p className="font-semibold">{user.full_name}</p>
                <p className="text-sm text-slate-500">{user.email}</p>
                <p className="text-sm text-slate-500">Role: {user.role}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
