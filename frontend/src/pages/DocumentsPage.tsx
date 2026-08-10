import { useEffect, useState } from "react";
import { fetchDocuments, DocumentItem } from "../services/documents";

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDocuments()
      .then(setDocuments)
      .catch((err) => {
        console.error("Error loading documents:", err);
        setError("Unable to load documents.");
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="rounded-3xl bg-white p-8 shadow-sm space-y-6">
      <div>
        <h1 className="text-3xl font-semibold text-slate-900">Knowledge Base Documents</h1>
        <p className="mt-2 text-slate-600">Uploaded documents available for AI knowledge-base retrieval.</p>
      </div>

      {loading ? (
        <p className="text-slate-500">Loading documents...</p>
      ) : error ? (
        <div className="rounded-2xl bg-red-50 p-4 text-sm text-red-700 border border-red-200">{error}</div>
      ) : documents.length === 0 ? (
        <p className="text-slate-500">No documents found.</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {documents.map((doc) => (
            <div key={doc.id} className="rounded-2xl border border-slate-200 p-5 transition hover:border-indigo-300">
              <p className="font-semibold text-slate-900 truncate">{doc.filename}</p>
              <p className="mt-3 text-sm text-slate-500">Uploaded: {new Date(doc.created_at).toLocaleDateString()}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
