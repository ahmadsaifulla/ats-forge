export interface ParsedResume {
  resume_id: string;
  filename: string;
  text: string;
  sections: Record<string, string>;
  detected_file_type: "pdf" | "docx";
  warnings: string[];
}

export interface ResumeUploadResponse {
  resume: ParsedResume;
}

export interface ScoreBreakdown {
  keyword_score: number;
  semantic_score: number;
  structure_score: number;
}

export interface AnalysisResponse {
  resume_id: string;
  total_score: number;
  breakdown: ScoreBreakdown;
  missing_keywords: string[];
  matched_keywords: string[];
  suggestions: string[];
  keyword_insights: {
    exact_keywords: string[];
    normalized_keywords: string[];
    inferred_skills: string[];
    missing_skills: string[];
    skill_frequencies: Record<string, number>;
    stuffing_penalty: number;
  };
}

export interface OptimizedResumeSection {
  title: string;
  content: string[];
  labels?: Array<"Rewritten content" | "Suggested additions">;
  items?: Array<{ label: "Rewritten content" | "Suggested additions"; text: string }>;
}

export interface OptimizedResume {
  resume_id: string;
  document_id: string;
  plain_text: string;
  sections: OptimizedResumeSection[];
  disclaimer: string;
  generated_at: string;
}

export interface OptimizeResponse {
  original_analysis: AnalysisResponse;
  optimized_analysis: AnalysisResponse;
  optimized_resume: OptimizedResume;
}
