import type { PropsWithChildren } from "react";
import { Link, useLocation } from "react-router-dom";
import clsx from "clsx";

const steps = [
  { href: "/", label: "Upload" },
  { href: "/analysis", label: "Analyze" },
  { href: "/optimized", label: "Optimize" },
];

export function AppShell({ children }: PropsWithChildren) {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-hero-grid text-ink">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8">
        <header className="mb-8 rounded-[2rem] border border-white/70 bg-white/70 px-6 py-5 shadow-panel backdrop-blur">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="font-display text-sm uppercase tracking-[0.35em] text-pine">ATS Forge</p>
              <h1 className="mt-2 font-display text-3xl leading-tight sm:text-4xl">
                Turn a generic resume into a role-targeted, ATS-friendly submission.
              </h1>
            </div>
            <nav className="flex gap-2 self-start rounded-full bg-mist p-2">
              {steps.map((step) => (
                <Link
                  key={step.href}
                  className={clsx(
                    "rounded-full px-4 py-2 text-sm font-semibold transition",
                    location.pathname === step.href
                      ? "bg-ink text-white"
                      : "text-ink/70 hover:bg-white",
                  )}
                  to={step.href}
                >
                  {step.label}
                </Link>
              ))}
            </nav>
          </div>
        </header>
        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
}
