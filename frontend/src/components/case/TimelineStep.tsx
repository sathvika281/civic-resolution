import { formatDate } from '../../lib/format'
import type { TimelineEntryOut } from '../../lib/types'
import { StatusIcon } from '../common/StatusIcon'

export function TimelineStep({ entry, isLast }: { entry: TimelineEntryOut; isLast: boolean }) {
  return (
    <div className="flex gap-3">
      <div className="flex flex-col items-center">
        <StatusIcon status={entry.status} />
        {!isLast && <span className="mt-1 w-px flex-1 bg-ink-200" />}
      </div>
      <div className={`pb-5 ${entry.status === 'pending' ? 'text-ink-400' : 'text-ink-800'}`}>
        <p className="text-sm font-medium">{entry.stage_name}</p>
        <p className="text-xs text-ink-400">
          {formatDate(entry.occurred_at)}
          {entry.actor_name ? ` · ${entry.actor_name}` : ''}
        </p>
        {entry.note && <p className="mt-1 text-xs text-ink-500">{entry.note}</p>}
      </div>
    </div>
  )
}
