import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useEffect } from "react";

export default function HomePage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  // If already logged in, redirect directly to the dashboard
  /*
  useEffect(() => {
    if (user) {
      navigate("/app/dashboard", { replace: true });
    }
  }, [user, navigate]);
  */
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6 text-center">
      <h1 className="text-4xl font-extrabold text-gray-900 mb-4">
        AI Support & RAG Knowledge Platform
      </h1>
      <p className="text-lg text-gray-600 mb-8 max-w-xl">
        Automate support ticket management and extract insights from your enterprise documents with AI.
      </p>
      
      <div className="flex space-x-4">
        <Link
          to="/login"
          className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow hover:bg-blue-700 transition"
        >
          Log In
        </Link>
        <Link
          to="/register"
          className="px-6 py-3 bg-white text-blue-600 font-semibold border border-blue-600 rounded-lg shadow hover:bg-blue-50 transition"
        >
          Register
        </Link>
      </div>
    </div>
  );
}