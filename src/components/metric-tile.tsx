import type { LucideIcon } from "lucide-react";

const tones = {
  amber: "bg-[#fff4dc] text-[#7a4a00]",
  blue: "bg-[#e4f2ff] text-[#0c5599]",
  green: "bg-[#dff8e9] text-[#126137]",
  violet: "bg-[#ece9ff] text-[#4f46e5]",
};

interface MetricTileProps {
  icon: LucideIcon;
  label: string;
  value: string;
  detail: string;
  tone: keyof typeof tones;
}

export function MetricTile({ icon: Icon, label, value, detail, tone }: MetricTileProps) {
  return (
    <article className="rounded-md border border-[#c9ded1] bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-[#516070]">{label}</p>
          <p className="mt-2 font-mono text-3xl font-semibold text-[#15171c]">{value}</p>
        </div>
        <div className={`flex h-10 w-10 items-center justify-center rounded-md ${tones[tone]}`}>
          <Icon size={21} aria-hidden="true" />
        </div>
      </div>
      <p className="mt-4 min-h-10 text-sm leading-5 text-[#516070]">{detail}</p>
    </article>
  );
}
