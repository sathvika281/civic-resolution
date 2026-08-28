import { Link } from 'react-router-dom'
import { formatCategory } from '../../lib/format'
import type { NearbyProblemOut } from '../../lib/types'
import { StatusDot } from '../common/StatusIcon'

export function NearbyProblemsList({ problems }: { problems: NearbyProblemOut[] }) {
  if (problems.length === 0) {
    return <p className="text-sm text-ink-400">No community reports nearby yet.</p>
  }

  const unresolvedCount = problems.filter((p) => p.status !== 'closed').length

  return (
    <div className="flex flex-col gap-2">
      <p className="text-sm text-ink-500">{unresolvedCount} unresolved issue{unresolvedCount === 1 ? '' : 's'} reported nearby</p>
      {problems.slice(0, 6).map((p) => (
        <Link
          key={p.case_number}
          to={`/case/${p.case_number}`}
          className="flex items-center justify-between rounded-2xl bg-white p-4 shadow-sm ring-1 ring-ink-100 transition hover:ring-brand-200"
        >
          <div className="flex items-center gap-3">
            <StatusDot status={p.status} />
            <div>
              <p className="font-medium text-ink-900">{p.issue_summary}</p>
              <p className="mt-0.5 text-xs text-ink-500">
                {formatCategory(p.category)} {p.location_text ? `· ${p.location_text}` : ''} · {p.affected_count} affected
              </p>
            </div>
          </div>
          {p.is_overdue && <span className="text-danger-500">⚠</span>}
        </Link>
      ))}
    </div>
  )
}
