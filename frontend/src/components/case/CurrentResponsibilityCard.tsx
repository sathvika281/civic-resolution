import type { CurrentResponsibilityOut } from '../../lib/types'

export function CurrentResponsibilityCard({ responsibility }: { responsibility: CurrentResponsibilityOut }) {
  return (
    <section className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-ink-100">
      <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">Who has this right now</p>
      <p className="mt-2 text-base font-semibold text-ink-900">{responsibility.authority_name}</p>
      <p className="text-sm text-ink-600">{responsibility.role} · {responsibility.jurisdiction_area}</p>
      <p className="mt-1 text-xs text-ink-400">
        At this stage for {responsibility.days_at_current_stage} day{responsibility.days_at_current_stage === 1 ? '' : 's'}
      </p>
    </section>
  )
}
