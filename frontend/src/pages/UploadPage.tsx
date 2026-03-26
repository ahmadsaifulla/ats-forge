import { ArrowRight, LoaderCircle } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Dropzone } from "../components/Dropzone";
import { uploadResume } from "../services/api";
import { saveState } from "../lib/storage";

export function UploadPage() {
  const navigate = useNavigate();
  const [fileName, setFileName] = useState<string | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleFile(file: File) {
    setErrorMessage(null);
    setIsLoading(true);
    setFileName(file.name);

    try {
      const response = await uploadResume(file);
      saveState("resume", response.resume);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Upload failed.");
    } finally {
      setIsLoading(false);
    }
  }

  function handleContinue() {
    if (!jobDescription.trim()) {
      setErrorMessage("Paste a job description before continuing.");
      return;
    }

    saveState("jobDescription", jobDescription);
    navigate("/analysis");
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
      <section className="rounded-[2rem] bg-white/80 p-6 shadow-panel sm:p-8">
        <Dropzone disabled={isLoading} fileName={fileName} onFileSelected={handleFile} />
        <label className="mt-6 block">
          <span className="text-sm font-semibold uppercase tracking-[0.22em] text-ink/65">Job Description</span>
          <textarea
            className="mt-3 min-h-[240px] w-full rounded-[1.5rem] border border-pine/15 bg-mist/40 px-4 py-4 text-base outline-none transition focus:border-pine focus:ring-2 focus:ring-pine/20"
            onChange={(event) => setJobDescription(event.target.value)}
            placeholder="Paste the target job description here..."
            value={jobDescription}
          />
        </label>
        {errorMessage ? <p className="mt-4 text-sm font-semibold text-clay">{errorMessage}</p> : null}
        <div className="mt-6 flex flex-wrap gap-3">
          <button
            className="inline-flex items-center gap-2 rounded-full bg-ink px-5 py-3 font-semibold text-white transition hover:bg-pine disabled:cursor-not-allowed disabled:opacity-60"
            disabled={isLoading}
            onClick={handleContinue}
            type="button"
          >
            {isLoading ? <LoaderCircle className="h-5 w-5 animate-spin" /> : <ArrowRight className="h-5 w-5" />}
            Continue to Analysis
          </button>
        </div>
      </section>
      <aside className="space-y-6">
        <div className="rounded-[2rem] bg-ink p-6 text-white shadow-panel">
          <p className="text-sm uppercase tracking-[0.3em] text-white/65">Workflow</p>
          <ol className="mt-4 space-y-4 text-sm leading-6 text-white/88">
            <li>1. Upload a PDF or DOCX resume that contains real text.</li>
            <li>2. Paste a target job description for role-specific analysis.</li>
            <li>3. Review ATS score, keyword gaps, and structure guidance.</li>
            <li>4. Generate a safer optimized resume and download it as DOCX.</li>
          </ol>
        </div>
        <div className="rounded-[2rem] bg-white/80 p-6 shadow-panel">
          <h2 className="font-display text-2xl">Built for real submissions</h2>
          <p className="mt-3 text-sm leading-6 text-ink/75">
            The optimizer keeps original meaning intact, avoids invented experience, and shows which keywords still need manual review.
          </p>
        </div>
      </aside>
    </div>
  );
}
