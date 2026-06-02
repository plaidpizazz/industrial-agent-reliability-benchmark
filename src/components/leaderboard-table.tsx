import type { LeaderboardRow } from "@/types/results";

import { ScoreBar } from "./score-bar";

interface LeaderboardTableProps {
  leaderboard: LeaderboardRow[];
}

export function LeaderboardTable({ leaderboard }: LeaderboardTableProps) {
  return (
    <section className="rounded-md border border-[#d9dde7] bg-white p-5 shadow-sm">
      <div>
        <h2 className="text-xl font-semibold text-[#15171c]">Leaderboard</h2>
        <p className="mt-1 text-sm leading-6 text-[#516070]">
          Composite reliability across multi-step agent trajectories, final answers, and governance markers.
        </p>
      </div>
      <div className="mt-5 overflow-x-auto">
        <table className="w-full min-w-[720px] border-collapse text-left text-sm">
          <thead>
            <tr className="border-b border-[#d9dde7] text-xs uppercase tracking-[0.12em] text-[#687589]">
              <th className="py-3 pr-4 font-semibold">Agent</th>
              <th className="px-4 py-3 font-semibold">Composite</th>
              <th className="px-4 py-3 font-semibold">Task</th>
              <th className="px-4 py-3 font-semibold">Tools</th>
              <th className="px-4 py-3 font-semibold">Loops</th>
              <th className="px-4 py-3 font-semibold">Governance</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((row) => (
              <tr key={row.agent} className="border-b border-[#eef1f5] last:border-0">
                <td className="py-4 pr-4">
                  <p className="font-semibold text-[#15171c]">{row.agent}</p>
                  <p className="text-xs text-[#687589]">{row.scenario_count} scenarios</p>
                </td>
                <td className="px-4 py-4">
                  <ScoreBar label="Composite" value={row.composite_score} hideLabel />
                </td>
                <td className="px-4 py-4 font-mono text-[#303640]">{Math.round(row.task_completion * 100)}%</td>
                <td className="px-4 py-4 font-mono text-[#303640]">{Math.round(row.tool_call_accuracy * 100)}%</td>
                <td className="px-4 py-4 font-mono text-[#303640]">{Math.round(row.loop_termination * 100)}%</td>
                <td className="px-4 py-4 font-mono text-[#303640]">{Math.round(row.governance * 100)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
