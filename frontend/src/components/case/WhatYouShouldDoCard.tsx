import type { CaseExplanation } from '../../lib/types'

export function WhatYouShouldDoCard({ explanation }: { explanation: CaseExplanation }) {
  return (
    <section className="rounded-2xl bg-brand-50 p-4 ring-1 ring-brand-100">
      <p className="text-xs font-semibold uppercase tracking-wide text-brand-700">What you should do</p>
      <p className="mt-2 text-sm font-medium text-ink-900">{explanation.what_you_should_do}</p>
      {explanation.then_step_label !== '-' && (
        <p className="mt-3 text-xs text-ink-500">
          What happens next: <span className="font-medium text-ink-700">{explanation.next_step_label}</span>
          {' → '}
          <span className="font-medium text-ink-700">{explanation.then_step_label}</span>
        </p>
      )}
    </section>
  )
}
