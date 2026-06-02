import type { PublicScenario } from "@/types/results";

interface ScenarioCoverageProps {
  scenarios: PublicScenario[];
}

const riskStyles = {
  high: "bg-[#ffe4de] text-[#8c2d18]",
  low: "bg-[#e1f7ea] text-[#126137]",
  medium: "bg-[#fff1d6] text-[#7a4a00]",
};

export function ScenarioCoverage({ scenarios }: ScenarioCoverageProps) {
  return (
    <section className="rounded-md border border-[#d9dde7] bg-white p-5 shadow-sm">
      <div>
        <h2 className="text-xl font-semibold text-[#15171c]">Scenario Coverage</h2>
        <p className="mt-1 text-sm leading-6 text-[#516070]">
          Synthetic aerospace tasks designed to evaluate tool selection, evidence grounding, and escalation behavior.
        </p>
      </div>
      <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {scenarios.map((scenario) => (
          <article key={scenario.id} className="rounded-md border border-[#e1e5ec] bg-[#fbfcfd] p-4">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="font-mono text-xs text-[#687589]">{scenario.id}</p>
                <h3 className="mt-2 text-sm font-semibold leading-5 text-[#15171c]">{scenario.title}</h3>
              </div>
              <span className={`rounded-md px-2 py-1 text-xs font-medium ${riskStyles[scenario.risk_level]}`}>
                {scenario.risk_level}
              </span>
            </div>
            <p className="mt-3 text-xs uppercase tracking-[0.12em] text-[#687589]">
              {scenario.category.replaceAll("_", " ")}
            </p>
            <div className="mt-3 flex flex-wrap gap-2">
              {scenario.expected_tool_calls.map((call) => (
                <span key={`${scenario.id}-${call.name}`} className="rounded-md bg-[#eef1f5] px-2 py-1 font-mono text-xs text-[#303640]">
                  {call.name}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
