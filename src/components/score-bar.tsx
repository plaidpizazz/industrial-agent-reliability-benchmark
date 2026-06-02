interface ScoreBarProps {
  label: string;
  value: number;
  compact?: boolean;
  hideLabel?: boolean;
}

export function ScoreBar({ label, value, compact = false, hideLabel = false }: ScoreBarProps) {
  const percentage = Math.max(0, Math.min(100, Math.round(value * 100)));

  return (
    <div className={compact ? "space-y-1" : "space-y-2"}>
      {!hideLabel && (
        <div className="flex items-center justify-between gap-3">
          <span className={compact ? "text-xs capitalize text-[#516070]" : "text-sm text-[#303640]"}>{label}</span>
          <span className={compact ? "font-mono text-xs text-[#303640]" : "font-mono text-sm font-semibold text-[#15171c]"}>
            {percentage}%
          </span>
        </div>
      )}
      <div className={compact ? "h-2 rounded-sm bg-[#e8ebf0]" : "h-3 rounded-sm bg-[#e8ebf0]"}>
        <div
          className="h-full rounded-sm bg-[#20a35a]"
          style={{ width: `${percentage}%` }}
          aria-label={`${label}: ${percentage}%`}
        />
      </div>
    </div>
  );
}
