import type { AnalysisResponse, OptimizeResponse, ResumeUploadResponse } from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

function getNetworkErrorMessage(error: unknown): string {
  if (error instanceof DOMException && error.name === "AbortError") {
    return "The request timed out while contacting the backend. Please try again.";
  }

  if (error instanceof TypeError) {
    return `Cannot reach the backend API at ${API_BASE_URL}. Make sure the FastAPI server is running and VITE_API_BASE_URL is correct.`;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "Request failed.";
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({ reason: "Request failed." }));
    throw new Error(errorBody.reason ?? errorBody.detail ?? "Request failed.");
  }
  return response.json() as Promise<T>;
}

export async function uploadResume(file: File): Promise<ResumeUploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 30000);

  try {
    const response = await fetch(`${API_BASE_URL}/upload-resume`, {
      method: "POST",
      body: formData,
      signal: controller.signal,
    });
    return await handleResponse<ResumeUploadResponse>(response);
  } catch (error) {
    throw new Error(getNetworkErrorMessage(error));
  } finally {
    window.clearTimeout(timeout);
  }
}

export async function analyzeResume(resumeId: string, jobDescription: string): Promise<AnalysisResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume_id: resumeId, job_description: jobDescription }),
    });

    return await handleResponse<AnalysisResponse>(response);
  } catch (error) {
    throw new Error(getNetworkErrorMessage(error));
  }
}

export async function optimizeResume(resumeId: string, jobDescription: string): Promise<OptimizeResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/optimize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume_id: resumeId, job_description: jobDescription }),
    });

    return await handleResponse<OptimizeResponse>(response);
  } catch (error) {
    throw new Error(getNetworkErrorMessage(error));
  }
}

export function getDownloadUrl(documentId: string) {
  return `${API_BASE_URL}/download/${documentId}`;
}
