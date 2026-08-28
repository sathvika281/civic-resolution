import { formatCategory } from '../../lib/format'
import type { ProblemUnderstanding } from '../../lib/types'

const URGENCY_LABELS: Record<string, string> = { low: 'Low', medium: 'Medium', high: 'High' }

export function UnderstandingSummary({ understanding }: { understanding: ProblemUnderstanding }) {
  return (
    <section className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-ink-100">
      <p className="text-xs font-semibold uppercase tracking-wide text-brand-600">We understood your problem</p>
      <dl className="mt-3 grid grid-cols-2 gap-3 text-sm">
        <div>
          <dt className="text-ink-400">Issue</dt>
          <dd className="font-medium text-ink-900">{understanding.issue_summary}</dd>
        </div>
        <div>
          <dt className="text-ink-400">Category</dt>
          <dd className="font-medium text-ink-900">{formatCategory(understanding.category)}</dd>
        </div>
        <div>
          <dt className="text-ink-400">Location</dt>
          <dd className="font-medium text-ink-900">{understanding.location_text ?? 'Not specified'}</dd>
        </div>
        <div>
          <dt className="text-ink-400">Priority</dt>
          <dd className="font-medium text-ink-900">{URGENCY_LABELS[understanding.urgency]}</dd>
        </div>
      </dl>
      {understanding.source === 'fallback' && (
        <p className="mt-3 text-[11px] text-ink-400">
          Understood using this prototype's deterministic rules engine, not a live AI call.
        </p>
      )}
    </section>
  )
}
