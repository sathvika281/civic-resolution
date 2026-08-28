import { formatDate } from '../../lib/format'
import type { EvidenceOut } from '../../lib/types'

export function EvidenceList({ evidence }: { evidence: EvidenceOut[] }) {
  if (evidence.length === 0) return null

  return (
    <section className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-ink-100">
      <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">Evidence</p>
      <div className="mt-3 flex flex-col gap-3">
        {evidence.map((e) => (
          <div key={e.id} className="rounded-xl bg-ink-50 p-3 text-sm">
            <p className="font-medium text-ink-800">{e.file_name}</p>
            {e.description_text && <p className="text-ink-500">{e.description_text}</p>}
            {e.interpretation && (
              <div className="mt-2 border-t border-ink-200 pt-2 text-xs text-ink-600">
                <p>🔎 {e.interpretation.likely_shows}</p>
                {e.interpretation.missing_info_hint && <p className="mt-1 text-warn-500">⚠ {e.interpretation.missing_info_hint}</p>}
              </div>
            )}
            <p className="mt-1 text-[11px] text-ink-400">{formatDate(e.created_at)}</p>
          </div>
        ))}
      </div>
      <p className="mt-2 text-[11px] text-ink-400">AI evidence analysis is for guidance only and is not a legal or final determination.</p>
    </section>
  )
}
