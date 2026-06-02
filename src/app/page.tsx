import {
  Activity,
  ArrowUpRight,
  BrainCircuit,
  CheckCircle2,
  GitBranch,
  ListChecks,
  Route,
  ShieldCheck,
  TriangleAlert,
} from "lucide-react";

import { LeaderboardTable } from "@/components/leaderboard-table";
import { MetricTile } from "@/components/metric-tile";
import { ScenarioCoverage } from "@/components/scenario-coverage";
import { ScoreBar } from "@/components/score-bar";
import { benchmarkSummary, categorySummaries, failureExamples, metricRows } from "@/lib/results";

const githubUrl = "https://github.com/plaidpizazz/industrial-agent-reliability-benchmark";

export default function Home() {
  const topAgent = benchmarkSummary.leaderboard[0];

  return (
    <main className="min-h-screen bg-[#f7f8fb] text-[#15171c]">
      <header className="border-b border-[#d9dde7] bg-white/90">
        <div className="mx-auto flex w-full max-w-7xl flex-col gap-5 px-5 py-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.14em] text-[#516070]">
              Industrial Agent Reliability Benchmark
            </p>
            <h1 className="mt-2 text-3xl font-semibold leading-tight text-[#15171c] md:text-4xl">
              Industrial Agent Reliability Benchmark
            </h1>
            <p className="mt-3 max-w-3xl text-base leading-7 text-[#516070]">
              A reproducible benchmark for multi-step agent behavior across synthetic aerospace supply chain,
              regulatory, and bid/no-bid workflows.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <a
              className="inline-flex h-11 items-center gap-2 rounded-md border border-[#cfd5df] bg-white px-4 text-sm font-medium text-[#15171c] shadow-sm transition hover:border-[#9aa8b8]"
              href={githubUrl}
              target="_blank"
              rel="noreferrer"
            >
              <GitBranch size={18} aria-hidden="true" />
              GitHub
              <ArrowUpRight size={16} aria-hidden="true" />
            </a>
            <a
              className="inline-flex h-11 items-center gap-2 rounded-md bg-[#15171c] px-4 text-sm font-medium text-white shadow-sm transition hover:bg-[#2a2e36]"
              href="#methodology"
            >
              <ListChecks size={18} aria-hidden="true" />
              Methodology
            </a>
          </div>
        </div>
      </header>

      <section className="border-b border-[#d9dde7] bg-[#edf7f1]">
        <div className="mx-auto grid w-full max-w-7xl gap-5 px-5 py-6 lg:grid-cols-[1fr_360px] lg:px-8">
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <MetricTile
              icon={ShieldCheck}
              label="Reliability score"
              value={`${Math.round(topAgent.composite_score * 100)}%`}
              detail={`${topAgent.agent} across ${topAgent.scenario_count} scenarios`}
              tone="green"
            />
            <MetricTile
              icon={Route}
              label="Tool-call accuracy"
              value={`${Math.round(topAgent.tool_call_accuracy * 100)}%`}
              detail="Expected tool sequence and allowed tool use"
              tone="blue"
            />
            <MetricTile
              icon={Activity}
              label="Loop termination"
              value={`${Math.round(topAgent.loop_termination * 100)}%`}
              detail="Stops inside scenario max-step budgets"
              tone="violet"
            />
            <MetricTile
              icon={TriangleAlert}
              label="Hallucination rate"
              value={`${Math.round(topAgent.hallucination_rate * 100)}%`}
              detail="Forbidden or unsupported claims"
              tone="amber"
            />
          </div>

          <div className="rounded-md border border-[#c9ded1] bg-white p-5 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-md bg-[#d9fbe6] text-[#126137]">
                <CheckCircle2 size={21} aria-hidden="true" />
              </div>
              <div>
                <p className="text-sm font-semibold text-[#15171c]">Governance gate</p>
                <p className="text-sm text-[#516070]">Passes deterministic reference threshold</p>
              </div>
            </div>
            <div className="mt-5 space-y-4">
              {metricRows.map((metric) => (
                <ScoreBar key={metric.label} label={metric.label} value={metric.value} />
              ))}
            </div>
          </div>
        </div>
      </section>

      <div className="mx-auto grid w-full max-w-7xl gap-8 px-5 py-8 lg:px-8">
        <section className="grid gap-5 lg:grid-cols-[1.1fr_0.9fr]">
          <LeaderboardTable leaderboard={benchmarkSummary.leaderboard} />
          <div className="rounded-md border border-[#d9dde7] bg-white p-5 shadow-sm">
            <div className="flex items-center gap-3">
              <BrainCircuit size={22} className="text-[#4f46e5]" aria-hidden="true" />
              <div>
                <h2 className="text-lg font-semibold text-[#15171c]">Benchmark scope</h2>
                <p className="text-sm text-[#516070]">
                  {benchmarkSummary.benchmark.scenario_count} synthetic scenarios, {benchmarkSummary.benchmark.agent_count} baselines
                </p>
              </div>
            </div>
            <div className="mt-5 grid gap-3">
              {categorySummaries.map((category) => (
                <div
                  key={category.name}
                  className="flex items-center justify-between rounded-md border border-[#e1e5ec] bg-[#fbfcfd] px-4 py-3"
                >
                  <div>
                    <p className="text-sm font-medium capitalize text-[#15171c]">
                      {category.name.replaceAll("_", " ")}
                    </p>
                    <p className="text-xs text-[#687589]">{category.risks.join(", ")} risk coverage</p>
                  </div>
                  <span className="font-mono text-lg font-semibold text-[#15171c]">{category.count}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        <ScenarioCoverage scenarios={benchmarkSummary.scenarios} />

        <section className="rounded-md border border-[#d9dde7] bg-white p-5 shadow-sm">
          <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
            <div>
              <h2 className="text-xl font-semibold text-[#15171c]">Failure Mode Examples</h2>
              <p className="mt-1 text-sm leading-6 text-[#516070]">
                The negative-control agent proves the harness catches repeated calls, missing escalation, and unsupported claims.
              </p>
            </div>
            <p className="font-mono text-xs uppercase tracking-[0.12em] text-[#687589]">
              generated {benchmarkSummary.generated_at}
            </p>
          </div>
          <div className="mt-5 grid gap-4 lg:grid-cols-3">
            {failureExamples.map((example) => (
              <article key={example.scenario_id} className="rounded-md border border-[#e1e5ec] bg-[#fbfcfd] p-4">
                <div className="flex items-center justify-between gap-3">
                  <p className="font-mono text-xs text-[#687589]">{example.scenario_id}</p>
                  <span className="rounded-md bg-[#fff1d6] px-2 py-1 font-mono text-xs text-[#7a4a00]">
                    {Math.round(example.composite_score * 100)}%
                  </span>
                </div>
                <p className="mt-3 text-sm leading-6 text-[#303640]">{example.final_answer}</p>
                <div className="mt-4 space-y-2">
                  {Object.values(example.metrics).map((metric) => (
                    <ScoreBar key={metric.name} label={metric.name.replaceAll("_", " ")} value={metric.score} compact />
                  ))}
                </div>
              </article>
            ))}
          </div>
        </section>

        <section id="methodology" className="rounded-md border border-[#d9dde7] bg-white p-5 shadow-sm">
          <h2 className="text-xl font-semibold text-[#15171c]">Methodology</h2>
          <div className="mt-5 grid gap-5 lg:grid-cols-2">
            <div>
              <h3 className="text-sm font-semibold uppercase tracking-[0.12em] text-[#516070]">Metrics</h3>
              <dl className="mt-3 grid gap-3">
                {Object.entries(benchmarkSummary.benchmark.metric_weights).map(([metric, weight]) => (
                  <div key={metric} className="flex items-center justify-between border-b border-[#e8ebf0] pb-2">
                    <dt className="text-sm capitalize text-[#303640]">{metric.replaceAll("_", " ")}</dt>
                    <dd className="font-mono text-sm font-semibold text-[#15171c]">{Math.round(weight * 100)}%</dd>
                  </div>
                ))}
              </dl>
            </div>
            <div>
              <h3 className="text-sm font-semibold uppercase tracking-[0.12em] text-[#516070]">Reproduce</h3>
              <div className="mt-3 rounded-md border border-[#20242b] bg-[#15171c] p-4 font-mono text-sm leading-7 text-[#d7f8e4]">
                <p>npm install</p>
                <p>python -m pip install -e .[dev]</p>
                <p>npm run eval:demo</p>
                <p>npm run build</p>
              </div>
              <p className="mt-3 text-sm leading-6 text-[#516070]">
                Claude and LangSmith adapters are optional. CI uses deterministic baselines so public checks avoid API cost and secret exposure.
              </p>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
