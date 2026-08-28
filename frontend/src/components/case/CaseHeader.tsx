import { formatStatus } from '../../lib/format'
import type { CaseStatus } from '../../lib/types'

const STATUS_STYLES: Record<CaseStatus, string> = {
  open: 'bg-danger-500/10 text-danger-600',
  in_progress: 'bg-warn-500/10 text-warn-500',
  resolved_pending_verification: 'bg-brand-500/10 text-brand-600',
  closed: 'bg-ok-500/10 text-ok-500',
  reopened: 'bg-danger-500/10 text-danger-600',
}

export function CaseHeader({ issueSummary, caseNumber, status }: { issueSummary: string; caseNumber: string; status: CaseStatus }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wide text-ink-400">Case {caseNumber}</p>
      <div className="mt-1 flex items-center justify-between gap-3">
        <h1 className="text-xl font-semibold text-ink-900">{issueSummary}</h1>
        <span className={`shrink-0 rounded-full px-3 py-1 text-xs font-semibold ${STATUS_STYLES[status]}`}>
          {formatStatus(status)}
        </span>
      </div>
    </div>
  )
}
