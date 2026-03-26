interface KeywordPillsProps {
  title: string;
  items: string[];
  tone?: "default" | "missing";
}

export function KeywordPills({ title, items, tone = "default" }: KeywordPillsProps) {
  return (
    <section className="rounded-[1.5rem] bg-white/80 p-5 shadow-panel">
      <h3 className="font-display text-xl">{title}</h3>
      <div className="mt-4 flex flex-wrap gap-2">
        {items.length ? (
          items.map((item) => (
            <span
              className={`rounded-full px-3 py-2 text-sm font-semibold ${
                tone === "missing" ? "bg-clay/15 text-clay" : "bg-pine/10 text-pine"
              }`}
              key={item}
            >
              {item}
            </span>
          ))
        ) : (
          <p className="text-sm text-ink/60">No items to show yet.</p>
        )}
      </div>
    </section>
  );
}
