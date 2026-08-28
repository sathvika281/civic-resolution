import type { SlaOut } from '../../lib/types'

export function SlaDelayBadge({ sla }: { sla: SlaOut }) {
  return (
    <section
      className={`rounded-2xl p-4 ring-1 ${
        sla.is_overdue ? 'bg-danger-500/5 ring-danger-500/20' : 'bg-white ring-ink-100 shadow-sm'
      }`}
    >
      <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">Resolution timeline</p>
      <div className="mt-2 flex items-center gap-6 text-sm">
        <div>
          <p className="text-ink-400">Expected</p>
          <p className="font-semibold text-ink-900">{sla.expected_days} days</p>
        </div>
        <div>
          <p className="text-ink-400">Current</p>
          <p className="font-semibold text-ink-900">{sla.current_days} days</p>
        </div>
      </div>
      {sla.is_overdue ? (
        <p className="mt-3 text-sm font-semibold text-danger-600">
          ⚠ {sla.days_overdue} day{sla.days_overdue === 1 ? '' : 's'} overdue
        </p>
      ) : (
        <p className="mt-3 text-sm font-medium text-ok-500">On track</p>
      )}
      <p className="mt-2 text-[11px] text-ink-400">{sla.note}</p>
    </section>
  )
}
