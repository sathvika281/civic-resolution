import { Link } from 'react-router-dom'
import type { RelatedCaseOut } from '../../lib/types'

export function RelatedCasesList({ relatedCases }: { relatedCases: RelatedCaseOut[] }) {
  if (relatedCases.length === 0) return null

  return (
    <section className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-ink-100">
      <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">Related reports</p>
      <div className="mt-2 flex flex-col gap-1.5">
        {relatedCases.map((rc) => (
          <Link key={rc.case_number} to={`/case/${rc.case_number}`} className="flex items-center justify-between text-sm text-brand-700 hover:underline">
            <span>{rc.issue_summary}{rc.location_text ? ` · ${rc.location_text}` : ''}</span>
            <span className="text-ink-300">›</span>
          </Link>
        ))}
      </div>
    </section>
  )
}
