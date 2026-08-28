import type { StageStatus } from '../../lib/types'

export function StatusIcon({ status }: { status: StageStatus }) {
  const map: Record<StageStatus, { symbol: string; className: string }> = {
    completed: { symbol: '✓', className: 'bg-ok-500 text-white' },
    current: { symbol: '!', className: 'bg-warn-500 text-white' },
    pending: { symbol: '', className: 'bg-ink-100 text-ink-400 ring-1 ring-inset ring-ink-300' },
    blocked: { symbol: '✕', className: 'bg-danger-500 text-white' },
  }
  const { symbol, className } = map[status]
  return (
    <span className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold ${className}`}>
      {symbol}
    </span>
  )
}

export function OverdueBadge({ daysOverdue }: { daysOverdue: number }) {
  if (daysOverdue <= 0) return null
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-danger-500/10 px-2.5 py-1 text-xs font-semibold text-danger-600">
      ⚠ {daysOverdue} day{daysOverdue === 1 ? '' : 's'} overdue
    </span>
  )
}

const DOT_COLORS: Record<string, string> = {
  open: 'bg-danger-500',
  in_progress: 'bg-warn-500',
  reopened: 'bg-danger-500',
  resolved_pending_verification: 'bg-brand-500',
  closed: 'bg-ok-500',
}

export function StatusDot({ status }: { status: string }) {
  return <span className={`inline-block h-2.5 w-2.5 rounded-full ${DOT_COLORS[status] ?? 'bg-ink-300'}`} />
}
