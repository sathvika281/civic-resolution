import { useState } from 'react'
import { api } from '../../lib/apiClient'
import type { CaseDetailOut, CommunityOut } from '../../lib/types'

interface Props {
  caseNumber: string
  citizenId: string
  community: CommunityOut
  onConfirmed: (updated: CaseDetailOut) => void
}

export function CommunityConfirmBar({ caseNumber, citizenId, community, onConfirmed }: Props) {
  const [confirming, setConfirming] = useState(false)
  const [confirmed, setConfirmed] = useState(false)

  const confirm = async () => {
    setConfirming(true)
    try {
      const updated = await api.post<CaseDetailOut>(`/api/cases/${caseNumber}/confirm`, { citizen_id: citizenId })
      onConfirmed(updated)
      setConfirmed(true)
    } finally {
      setConfirming(false)
    }
  }

  return (
    <section className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-ink-100">
      <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">Community</p>
      <p className="mt-2 text-sm text-ink-800">
        <span className="font-semibold">{community.affected_count}</span> citizens affected ·{' '}
        <span className="font-semibold">{community.confirmed_count}</span> confirmed
      </p>
      {community.cluster?.possible_common_issue && (
        <p className="mt-2 rounded-xl bg-accent-500/10 p-2.5 text-xs text-accent-600">🔗 {community.cluster.summary}</p>
      )}
      <button
        onClick={confirm}
        disabled={confirming || confirmed}
        className="mt-3 rounded-full bg-ink-100 px-4 py-1.5 text-sm font-medium text-ink-700 disabled:opacity-60"
      >
        {confirmed ? '✓ You confirmed this' : confirming ? 'Confirming…' : "This is happening to me too"}
      </button>
    </section>
  )
}
