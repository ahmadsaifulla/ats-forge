import { Download, RotateCcw } from "lucide-react";
import { Link, Navigate, useLocation } from "react-router-dom";
import { KeywordPills } from "../components/KeywordPills";
import { ScoreBars } from "../components/ScoreBars";
import { StatCard } from "../components/StatCard";
import { loadState } from "../lib/storage";
import { getDownloadUrl } from "../services/api";
import type { OptimizeResponse } from "../types/api";

const DEMO_OPTIMIZED: OptimizeResponse = {
  original_analysis: {
    resume_id: "demo-resume-1",
    total_score: 82,
    breakdown: { keyword_score: 88, semantic_score: 79, structure_score: 86 },
    missing_keywords: ["backend engineering", "problem solving", "scalable systems"],
    matched_keywords: ["python", "c++", "object oriented programming", "application programming interfaces"],
    suggestions: [
      "Strengthen the summary with explicit backend engineering language aligned to the target role.",
      "Keep quantified backend impact statements near the top of experience.",
      "Add scalable systems or performance work only if it is genuinely supported by prior projects.",
    ],
    keyword_insights: {
      exact_keywords: ["python", "c++", "object oriented programming"],
      normalized_keywords: ["python", "c++", "object oriented programming", "application programming interfaces"],
      inferred_skills: ["object oriented programming", "data analysis"],
      missing_skills: ["backend engineering", "problem solving", "scalable systems"],
      skill_frequencies: { python: 2, "c++": 1, "object oriented programming": 1, "application programming interfaces": 1 },
      stuffing_penalty: 0,
    },
  },
  optimized_analysis: {
    resume_id: "demo-resume-1",
    total_score: 93,
    breakdown: { keyword_score: 95, semantic_score: 90, structure_score: 91 },
    missing_keywords: ["scalable systems"],
    matched_keywords: ["python", "c++", "application programming interfaces", "object oriented programming", "backend engineering", "problem solving"],
    suggestions: ["Resume is strongly aligned; review one final time for role-specific wording and truthfulness."],
    keyword_insights: {
      exact_keywords: ["python", "c++", "object oriented programming"],
      normalized_keywords: ["python", "c++", "application programming interfaces", "object oriented programming", "backend engineering", "problem solving"],
      inferred_skills: ["object oriented programming", "data analysis"],
      missing_skills: ["scalable systems"],
      skill_frequencies: {
        python: 2,
        "c++": 1,
        "application programming interfaces": 1,
        "object oriented programming": 1,
        "backend engineering": 1,
        "problem solving": 1,
      },
      stuffing_penalty: 0,
    },
  },
  optimized_resume: {
    resume_id: "demo-resume-1",
    document_id: "demo-document-1",
    plain_text: "",
    disclaimer:
      "This version is optimized for ATS readability using clearer structure, evidence-based phrasing, and only role terms that can be reasonably grounded in the source resume.",
    generated_at: new Date().toISOString(),
    sections: [
      {
        title: "SUMMARY",
        content: [
          "Results-oriented backend engineer with experience building ATS-aligned APIs and object oriented programming solutions.",
          "Core strengths include Python, FastAPI, SQL, Docker, C++, backend systems, and recruiter workflow optimization.",
        ],
        labels: ["Rewritten content", "Rewritten content"],
        items: [
          { label: "Rewritten content", text: "Results-oriented backend developer with experience building ATS-aligned APIs and object oriented programming solutions." },
          { label: "Rewritten content", text: "Core strengths include Python, FastAPI, SQL, Docker, C++, and recruiter workflow optimization." },
        ],
      },
      {
        title: "SKILLS",
        content: ["Python", "FastAPI", "SQL", "Docker", "Object Oriented Programming", "C++"],
        labels: Array(6).fill("Rewritten content"),
        items: [
          { label: "Rewritten content", text: "Python" },
          { label: "Rewritten content", text: "FastAPI" },
          { label: "Rewritten content", text: "SQL" },
          { label: "Rewritten content", text: "Docker" },
          { label: "Rewritten content", text: "Object Oriented Programming" },
          { label: "Rewritten content", text: "C++" },
        ],
      },
      {
        title: "EXPERIENCE",
        content: [
          "Built backend APIs and optimized applicant review workflows for faster recruiter operations.",
          "Improved recruiter turnaround by 35% through cleaner application pipeline handling and stronger engineering ownership.",
        ],
        labels: ["Rewritten content", "Rewritten content"],
        items: [
          { label: "Rewritten content", text: "Built backend APIs and optimized ATS workflows for faster recruiter operations." },
          { label: "Rewritten content", text: "Improved recruiter turnaround by 35% through cleaner application pipeline handling." },
        ],
      },
      {
        title: "EDUCATION",
        content: ["BS Computer Science"],
        labels: ["Rewritten content"],
        items: [{ label: "Rewritten content", text: "BS Computer Science" }],
      },
      {
        title: "SUGGESTED ADDITIONS",
        content: ["Add scalable systems only if it is genuinely supported by your experience, projects, certifications, or training."],
        labels: ["Suggested additions"],
        items: [{ label: "Suggested additions", text: "Add scalable systems only if it is genuinely supported by your experience, projects, certifications, or training." }],
      },
    ],
  },
};

export function OptimizedResumePage() {
  const location = useLocation();
  const isDemoMode = new URLSearchParams(location.search).get("demo") === "1";
  const optimized = isDemoMode ? DEMO_OPTIMIZED : loadState<OptimizeResponse>("optimized");

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
                href={isDemoMode ? "#" : getDownloadUrl(optimized.optimized_resume.document_id)}
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
