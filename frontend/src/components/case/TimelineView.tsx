import type { TimelineEntryOut } from '../../lib/types'
import { TimelineStep } from './TimelineStep'

export function TimelineView({ timeline }: { timeline: TimelineEntryOut[] }) {
  return (
    <section className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-ink-100">
      <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">Timeline</p>
      <div className="mt-3">
        {timeline.map((entry, index) => (
          <TimelineStep key={`${entry.stage_name}-${index}`} entry={entry} isLast={index === timeline.length - 1} />
        ))}
      </div>
    </section>
  )
}
