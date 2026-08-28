import { Link } from 'react-router-dom'
import { formatCategory, formatStatus } from '../../lib/format'
import type { CaseSummaryOut } from '../../lib/types'

export function RecentCasesList({ cases }: { cases: CaseSummaryOut[] }) {
  if (cases.length === 0) {
    return <p className="text-sm text-ink-400">You don't have any cases yet. Tell us what's wrong above to start one.</p>
  }

  return (
    <div className="flex flex-col gap-2">
      {cases.map((c) => (
        <Link
          key={c.case_number}
          to={`/case/${c.case_number}`}
          className="flex items-center justify-between rounded-2xl bg-white p-4 shadow-sm ring-1 ring-ink-100 transition hover:ring-brand-200"
        >
          <div>
            <p className="font-medium text-ink-900">{c.issue_summary}</p>
            <p className="mt-0.5 text-xs text-ink-500">
              {c.case_number} · {formatCategory(c.category)} · {formatStatus(c.status)}
            </p>
          </div>
          {c.is_overdue && c.status !== 'closed' ? (
            <span className="text-danger-500">⚠</span>
          ) : (
            <span className="text-ink-300">›</span>
          )}
        </Link>
      ))}
    </div>
  )
}
