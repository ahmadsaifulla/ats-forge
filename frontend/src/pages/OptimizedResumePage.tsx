import { Download, RotateCcw } from "lucide-react";
import { Link, Navigate } from "react-router-dom";
import { KeywordPills } from "../components/KeywordPills";
import { ScoreBars } from "../components/ScoreBars";
import { StatCard } from "../components/StatCard";
import { loadState } from "../lib/storage";
import { getDownloadUrl } from "../services/api";
import type { OptimizeResponse } from "../types/api";

export function OptimizedResumePage() {
  const optimized = loadState<OptimizeResponse>("optimized");

  if (!optimized) {
    return <Navigate replace to="/" />;
  }

  const improvement = Math.max(
    0,
    Math.round(optimized.optimized_analysis.total_score - optimized.original_analysis.total_score),
  );

  return (
    <div className="space-y-6">
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Original ATS" value={`${optimized.original_analysis.total_score}%`} />
        <StatCard label="Optimized ATS" tone="positive" value={`${optimized.optimized_analysis.total_score}%`} />
        <StatCard label="Improvement" value={`+${improvement}`} />
        <StatCard label="Download" value="DOCX Ready" />
      </section>

      <section className="grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
        <div className="space-y-6">
          <div className="rounded-[2rem] bg-white/80 p-6 shadow-panel">
            <div className="flex flex-wrap gap-3">
              <a
                className="inline-flex items-center gap-2 rounded-full bg-ink px-5 py-3 font-semibold text-white transition hover:bg-pine"
                href={getDownloadUrl(optimized.optimized_resume.document_id)}
              >
                <Download className="h-5 w-5" />
                Download Optimized Resume
              </a>
              <Link
                className="inline-flex items-center gap-2 rounded-full border border-ink/15 bg-white px-5 py-3 font-semibold text-ink transition hover:border-pine hover:text-pine"
                to="/"
              >
                <RotateCcw className="h-5 w-5" />
                Start New Analysis
              </Link>
            </div>
            <p className="mt-5 rounded-[1.25rem] bg-sun/15 px-4 py-4 text-sm leading-6 text-ink/80">
              {optimized.optimized_resume.disclaimer}
            </p>
          </div>

          <ScoreBars breakdown={optimized.original_analysis.breakdown} />
          <ScoreBars breakdown={optimized.optimized_analysis.breakdown} />
          <KeywordPills items={optimized.original_analysis.missing_keywords} title="Still Missing Keywords" tone="missing" />
        </div>

        <section className="rounded-[2rem] bg-white/80 p-6 shadow-panel">
          <h2 className="font-display text-2xl">Optimized Resume Preview</h2>
          <div className="mt-6 space-y-6">
            {optimized.optimized_resume.sections.map((section) => (
              <div key={section.title} className="rounded-[1.5rem] border border-pine/10 bg-mist/30 p-5">
                <h3 className="font-display text-xl">{section.title}</h3>
                <div className="mt-3 space-y-3 text-sm leading-6 text-ink/80">
                  {section.content.map((line) => (
                    <p key={line}>{section.content.length > 1 ? `• ${line}` : line}</p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>
      </section>
    </div>
  );
}
