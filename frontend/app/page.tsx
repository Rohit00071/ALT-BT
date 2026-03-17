"use client";

import { useState, useRef } from "react";
import { useForm } from "react-hook-form";
import axios from "axios";

interface FormData {
  concept: string;
  language: string;
}

interface ApiResponse {
  status: "success" | "error";
  video_url?: string;
  message?: string;
  details?: string;
}

const LANGUAGES = [
  "English",
  "Hindi",
  "Spanish",
  "French",
  "German",
  "Arabic",
  "Japanese",
  "Chinese",
  "Korean",
  "Portuguese",
  "Russian",
  "Italian",
  "Turkish",
  "Bengali",
  "Tamil",
  "Telugu",
  "Urdu",
  "Thai",
  "Vietnamese",
  "Greek",
];

const EXAMPLE_CONCEPTS = [
  "Pythagorean Theorem",
  "Area of a Circle",
  "Quadratic Formula",
  "Sine and Cosine Waves",
  "Matrix Multiplication",
  "Derivative of x²",
  "Fibonacci Sequence",
  "Euler's Formula",
];

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [statusText, setStatusText] = useState("");
  const videoRef = useRef<HTMLVideoElement>(null);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<FormData>({
    defaultValues: {
      concept: "",
      language: "English",
    },
  });

  const onSubmit = async (data: FormData) => {
    setLoading(true);
    setVideoUrl(null);
    setError(null);
    setStatusText("✨ AI is writing Manim code…");

    try {
      // Simulate progress updates
      const progressTimer = setTimeout(() => {
        setStatusText("🎬 Rendering your animation with Manim…");
      }, 5000);

      const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";
      const response = await axios.post<ApiResponse>(`${apiBaseUrl}/api/generate_video`, {
        concept: data.concept.trim(),
        language: data.language,
      });

      clearTimeout(progressTimer);

      if (response.data.status === "success" && response.data.video_url) {
        const fullVideoUrl = response.data.video_url.startsWith("http")
          ? response.data.video_url
          : `${apiBaseUrl}${response.data.video_url}`;
        setVideoUrl(fullVideoUrl);
        setStatusText("");
        // Auto scroll to video
        setTimeout(() => {
          videoRef.current?.scrollIntoView({ behavior: "smooth", block: "center" });
        }, 300);
      } else {
        setError(response.data.message || "Something went wrong.");
        setStatusText("");
      }
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(
          err.response?.data?.message ||
            "Failed to connect to the server. Is the backend running?"
        );
      } else {
        setError("An unexpected error occurred.");
      }
      setStatusText("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-10 animate-fade-in-up">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-[var(--glass-border)] bg-[var(--glass-bg)] text-sm text-[var(--text-secondary)] mb-6 backdrop-blur-sm">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          Powered by AI + Manim
        </div>
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-4">
          <span className="bg-gradient-to-r from-violet-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
            Math Animator
          </span>
        </h1>
        <p className="text-lg md:text-xl text-[var(--text-secondary)] max-w-2xl mx-auto leading-relaxed">
          Type any math concept, pick a language, and watch AI create a
          beautiful educational animation in seconds.
        </p>
      </div>

      {/* Form Card */}
      <div
        className="glass-card w-full max-w-2xl p-8 md:p-10 animate-fade-in-up"
        style={{ animationDelay: "0.2s" }}
      >
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Concept Input */}
          <div>
            <label
              htmlFor="concept"
              className="block text-sm font-semibold text-[var(--text-secondary)] mb-2 uppercase tracking-wider"
            >
              Math Concept
            </label>
            <input
              id="concept"
              type="text"
              placeholder="e.g., Pythagorean Theorem, Area of a Circle…"
              className="w-full px-5 py-4 rounded-xl bg-white/5 border border-[var(--glass-border)] text-[var(--text-primary)] placeholder:text-[var(--text-muted)] focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500/50 transition-all duration-300 text-lg"
              {...register("concept", {
                required: "Please enter a math concept",
                maxLength: {
                  value: 300,
                  message: "Concept must be 300 characters or less",
                },
              })}
              disabled={loading}
            />
            {errors.concept && (
              <p className="mt-2 text-sm text-red-400">
                {errors.concept.message}
              </p>
            )}
            {/* Suggestion chips */}
            <div className="flex flex-wrap gap-2 mt-3">
              {EXAMPLE_CONCEPTS.map((example) => (
                <button
                  key={example}
                  type="button"
                  onClick={() => setValue("concept", example)}
                  className="px-3 py-1 text-xs rounded-full border border-[var(--glass-border)] bg-white/5 text-[var(--text-secondary)] hover:bg-violet-500/20 hover:border-violet-500/30 hover:text-violet-300 transition-all duration-200 cursor-pointer"
                  disabled={loading}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>

          {/* Language Select */}
          <div>
            <label
              htmlFor="language"
              className="block text-sm font-semibold text-[var(--text-secondary)] mb-2 uppercase tracking-wider"
            >
              Language
            </label>
            <select
              id="language"
              className="w-full px-5 py-4 rounded-xl bg-white/5 border border-[var(--glass-border)] text-[var(--text-primary)] focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500/50 transition-all duration-300 text-lg appearance-none cursor-pointer"
              style={{
                backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' fill='%2394a3b8' viewBox='0 0 24 24'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E")`,
                backgroundRepeat: "no-repeat",
                backgroundPosition: "right 16px center",
              }}
              {...register("language")}
              disabled={loading}
            >
              {LANGUAGES.map((lang) => (
                <option key={lang} value={lang} className="bg-gray-900">
                  {lang}
                </option>
              ))}
            </select>
          </div>

          {/* Generate Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 px-6 rounded-xl font-semibold text-lg text-white transition-all duration-300 cursor-pointer disabled:cursor-not-allowed relative overflow-hidden group"
            style={{
              background: loading
                ? "linear-gradient(135deg, #374151, #4b5563)"
                : "linear-gradient(135deg, #7c3aed, #6d28d9, #5b21b6)",
            }}
          >
            <span className="relative z-10 flex items-center justify-center gap-3">
              {loading ? (
                <>
                  <span className="spinner !w-5 !h-5 !border-2" />
                  Generating…
                </>
              ) : (
                <>
                  <svg
                    width="22"
                    height="22"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <polygon points="5 3 19 12 5 21 5 3" />
                  </svg>
                  Generate Animation
                </>
              )}
            </span>
            {!loading && (
              <span className="absolute inset-0 bg-gradient-to-r from-violet-600 to-purple-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            )}
          </button>
        </form>

        {/* Status / Loading */}
        {loading && statusText && (
          <div className="mt-8 text-center animate-fade-in-up">
            <div className="inline-flex items-center gap-3 px-6 py-3 rounded-2xl bg-violet-500/10 border border-violet-500/20">
              <span className="spinner !w-5 !h-5 !border-2" />
              <span className="text-violet-300 font-medium">{statusText}</span>
            </div>
            <div className="mt-4 w-full h-1.5 rounded-full overflow-hidden bg-white/5">
              <div className="shimmer-bar h-full rounded-full" />
            </div>
            <p className="mt-3 text-sm text-[var(--text-muted)]">
              This usually takes 20–60 seconds
              <span className="dot-1">.</span>
              <span className="dot-2">.</span>
              <span className="dot-3">.</span>
            </p>
          </div>
        )}

        {/* Error Display */}
        {error && !loading && (
          <div
            className="mt-8 p-5 rounded-2xl animate-fade-in-up"
            style={{
              background: "var(--error-bg)",
              border: "1px solid var(--error-border)",
            }}
          >
            <div className="flex items-start gap-3">
              <svg
                className="w-6 h-6 text-red-400 flex-shrink-0 mt-0.5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <circle cx="12" cy="12" r="10" />
                <line x1="15" y1="9" x2="9" y2="15" />
                <line x1="9" y1="9" x2="15" y2="15" />
              </svg>
              <div>
                <h3
                  className="font-semibold mb-1"
                  style={{ color: "var(--error-text)" }}
                >
                  Generation Failed
                </h3>
                <p className="text-sm text-red-300/80">{error}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Video Player */}
      {videoUrl && !loading && (
        <div
          className="w-full max-w-3xl mt-10 animate-fade-in-up"
          style={{ animationDelay: "0.1s" }}
        >
          <div className="glass-card p-6 md:p-8">
            <div className="flex items-center gap-3 mb-5">
              <div className="w-3 h-3 rounded-full bg-emerald-400 animate-pulse" />
              <h2 className="text-xl font-semibold text-[var(--text-primary)]">
                Your Animation is Ready!
              </h2>
            </div>
            <div className="rounded-2xl overflow-hidden bg-black/40">
              <video
                ref={videoRef}
                src={videoUrl}
                controls
                autoPlay
                className="w-full"
                style={{ maxHeight: "500px" }}
              >
                Your browser does not support the video tag.
              </video>
            </div>
            <div className="flex items-center justify-between mt-4">
              <p className="text-sm text-[var(--text-muted)]">
                Rendered with Manim Community Edition
              </p>
              <a
                href={videoUrl}
                download
                className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 border border-[var(--glass-border)] text-sm text-[var(--text-secondary)] hover:bg-white/10 hover:text-white transition-all duration-200"
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" y1="15" x2="12" y2="3" />
                </svg>
                Download MP4
              </a>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="mt-16 text-center text-sm text-[var(--text-muted)] animate-fade-in-up" style={{ animationDelay: "0.4s" }}>
        <p>
          Built with{" "}
          <span className="text-violet-400">Next.js</span> •{" "}
          <span className="text-cyan-400">FastAPI</span> •{" "}
          <span className="text-pink-400">Manim</span> •{" "}
          <span className="text-emerald-400">Gemini / Groq AI</span>
        </p>
        <p className="mt-1 text-[var(--text-muted)]/50">
          100% free & open-source — no paid APIs required
        </p>
      </footer>
    </main>
  );
}
