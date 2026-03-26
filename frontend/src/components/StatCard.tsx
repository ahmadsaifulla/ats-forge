interface StatCardProps {
  label: string;
  value: number | string;
  tone?: "default" | "positive" | "warning";
}

export function StatCard({ label, value, tone = "default" }: StatCardProps) {
  const toneClass =
    tone === "positive"
      ? "bg-pine text-white"
      : tone === "warning"
        ? "bg-clay text-white"
        : "bg-white";

  return (
    <div className={`rounded-[1.5rem] border border-white/70 px-5 py-4 shadow-panel ${toneClass}`}>
      <p className="text-sm uppercase tracking-[0.22em] opacity-70">{label}</p>
      <p className="mt-3 font-display text-3xl">{value}</p>
    </div>
  );
}
