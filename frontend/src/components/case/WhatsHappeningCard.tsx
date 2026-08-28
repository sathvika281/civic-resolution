import type { CaseExplanation } from '../../lib/types'

export function WhatsHappeningCard({ explanation }: { explanation: CaseExplanation }) {
  return (
    <section className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-ink-100">
      <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">What's happening</p>
      <p className="mt-2 text-sm text-ink-800">{explanation.whats_happening}</p>
      <div className="mt-3 rounded-xl bg-ink-50 p-3 text-sm">
        <p className="text-ink-500">Current blocker</p>
        <p className="font-medium text-ink-800">{explanation.current_blocker}</p>
      </div>
      <p className="mt-2 text-xs text-ink-500">Who needs to act: <span className="font-medium text-ink-700">{explanation.who_needs_to_act}</span></p>
    </section>
  )
}
