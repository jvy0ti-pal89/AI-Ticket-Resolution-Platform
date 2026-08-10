import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadDocument } from "../services/documents";

export default function UploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      await uploadDocument(file);
      navigate("/app/documents");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-2xl rounded-3xl bg-white p-8 shadow-sm">
      <h1 className="text-3xl font-semibold text-slate-900">Upload Knowledge Base Document</h1>
      <p className="mt-2 text-slate-600">Upload PDF or TXT files to enrich AI context responses.</p>

      {error && (
        <div className="mt-4 rounded-2xl bg-red-50 p-4 border border-red-200 text-sm text-red-600">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="mt-8 space-y-6">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Select Document (.pdf, .txt)</label>
          <input
            type="file"
            accept=".pdf,.txt"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="w-full rounded-2xl border border-slate-300 p-3 bg-slate-50 text-slate-700"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading || !file}
          className="rounded-2xl bg-indigo-600 px-6 py-3 text-white transition hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading ? "Uploading..." : "Upload Document"}
        </button>
      </form>
    </div>
  );
}
