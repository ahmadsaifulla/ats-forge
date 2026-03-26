import { ArrowRight, FileWarning, LoaderCircle } from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { KeywordPills } from "../components/KeywordPills";
import { ScoreBars } from "../components/ScoreBars";
import { StatCard } from "../components/StatCard";
import { loadState, saveState } from "../lib/storage";
import { analyzeResume, optimizeResume } from "../services/api";
import type { AnalysisResponse, ParsedResume, OptimizeResponse } from "../types/api";

export function AnalysisPage() {
  const navigate = useNavigate();
  const [resume] = useState<ParsedResume | null>(() => loadState("resume"));
  const [jobDescription] = useState<string>(() => loadState("jobDescription") ?? "");
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(() => loadState("analysis"));
  const [isLoading, setIsLoading] = useState(false);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!resume || !jobDescription) {
      navigate("/", { replace: true });
      return;
    }

    if (analysis) {
      return;
    }

    setIsLoading(true);
    analyzeResume(resume.resume_id, jobDescription)
      .then((response) => {
        setAnalysis(response);
        saveState("analysis", response);
      })
      .catch((error: Error) => setErrorMessage(error.message))
      .finally(() => setIsLoading(false));
  }, [analysis, jobDescription, navigate, resume]);

  async function handleOptimize() {
    if (!resume) return;

    setIsOptimizing(true);
    setErrorMessage(null);
    try {
      const response: OptimizeResponse = await optimizeResume(resume.resume_id, jobDescription);
      saveState("optimized", response);
      navigate("/optimized");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Optimization failed.");
    } finally {
      setIsOptimizing(false);
    }
  }

  if (!resume) {
    return null;
  }

  return (
    <div className="space-y-6">
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Resume File" value={resume.filename} />
        <StatCard label="Warnings" tone={resume.warnings.length ? "warning" : "default"} value={resume.warnings.length} />
        <StatCard label="Overall ATS" tone="positive" value={analysis ? `${analysis.total_score}%` : "Pending"} />
        <StatCard label="Missing Keywords" value={analysis?.missing_keywords.length ?? 0} />
      </section>

      <section className="grid gap-6 lg:grid-cols-[1fr_0.9fr]">
        <div className="space-y-6">
          <div className="rounded-[2rem] bg-white/80 p-6 shadow-panel">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm uppercase tracking-[0.22em] text-ink/65">Analysis</p>
                <h2 className="mt-2 font-display text-2xl">ATS fit against the target job</h2>
              </div>
              <button
                className="inline-flex items-center gap-2 rounded-full bg-ink px-5 py-3 font-semibold text-white transition hover:bg-pine disabled:cursor-not-allowed disabled:opacity-60"
                disabled={isLoading || isOptimizing || !analysis}
                onClick={handleOptimize}
                type="button"
              >
                {isOptimizing ? <LoaderCircle className="h-5 w-5 animate-spin" /> : <ArrowRight className="h-5 w-5" />}
                Optimize Resume
              </button>
            </div>

            {isLoading ? (
              <div className="mt-8 flex items-center gap-3 text-sm text-ink/75">
                <LoaderCircle className="h-5 w-5 animate-spin" />
                Running ATS analysis...
              </div>
            ) : analysis ? (
              <div className="mt-6">
                <ScoreBars breakdown={analysis.breakdown} />
              </div>
            ) : (
              <div className="mt-8 flex items-center gap-3 rounded-[1.2rem] bg-clay/10 p-4 text-sm text-clay">
                <FileWarning className="h-5 w-5" />
                Analysis is not available yet.
              </div>
            )}

            {errorMessage ? <p className="mt-4 text-sm font-semibold text-clay">{errorMessage}</p> : null}
          </div>

          <KeywordPills items={analysis?.missing_keywords ?? []} title="Missing Keywords" tone="missing" />
          <KeywordPills items={analysis?.matched_keywords ?? []} title="Matched Keywords" />
        </div>

        <div className="space-y-6">
          <section className="rounded-[2rem] bg-white/80 p-6 shadow-panel">
            <h3 className="font-display text-xl">Improvement Guidance</h3>
            <ul className="mt-4 space-y-3 text-sm leading-6 text-ink/75">
              {(analysis?.suggestions ?? ["Upload a resume and job description to generate ATS guidance."]).map((item) => (
                <li key={item} className="rounded-[1rem] bg-mist/60 px-4 py-3">
                  {item}
                </li>
              ))}
            </ul>
          </section>

          <section className="rounded-[2rem] bg-ink p-6 text-white shadow-panel">
            <h3 className="font-display text-xl">Detected Sections</h3>
            <div className="mt-4 grid gap-3 text-sm text-white/85">
              {Object.entries(resume.sections).map(([name, content]) => (
                <div className="rounded-[1rem] bg-white/8 px-4 py-3" key={name}>
                  <p className="font-semibold capitalize">{name}</p>
                  <p className="mt-1 line-clamp-4 text-white/75">{content}</p>
                </div>
              ))}
            </div>
          </section>
        </div>
      </section>
    </div>
  );
}
