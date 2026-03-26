const KEYS = {
  resume: "ats-forge.resume",
  analysis: "ats-forge.analysis",
  optimized: "ats-forge.optimized",
  jobDescription: "ats-forge.job-description",
};

export function saveState<T>(key: keyof typeof KEYS, value: T) {
  localStorage.setItem(KEYS[key], JSON.stringify(value));
}

export function loadState<T>(key: keyof typeof KEYS): T | null {
  const rawValue = localStorage.getItem(KEYS[key]);
  if (!rawValue) {
    return null;
  }

  try {
    return JSON.parse(rawValue) as T;
  } catch {
    return null;
  }
}
