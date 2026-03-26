import type { ScoreBreakdown } from "../types/api";

interface ScoreBarsProps {
  breakdown: ScoreBreakdown;
}

export function ScoreBars({ breakdown }: ScoreBarsProps) {
  const items = [
    { label: "Keyword Match", value: breakdown.keyword_score },
    { label: "Semantic Match", value: breakdown.semantic_score },
    { label: "Structure", value: breakdown.structure_score },
  ];

  return (
    <section className="rounded-[1.5rem] bg-white/80 p-5 shadow-panel">
      <h3 className="font-display text-xl">Score Breakdown</h3>
      <div className="mt-5 space-y-4">
        {items.map((item) => (
          <div key={item.label}>
            <div className="mb-2 flex items-center justify-between text-sm font-semibold">
              <span>{item.label}</span>
              <span>{item.value}%</span>
            </div>
            <div className="h-3 rounded-full bg-mist">
              <div
                className="h-3 rounded-full bg-gradient-to-r from-pine via-sun to-clay"
                style={{ width: `${Math.min(item.value, 100)}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
