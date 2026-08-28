import { useState } from 'react'
import { ErrorState } from '../components/common/EmptyState'
import { Spinner } from '../components/common/Spinner'
import { useFetch } from '../hooks/useFetch'
import { api } from '../lib/apiClient'
import { formatCategory, formatStatus } from '../lib/format'
import type { CaseSummaryOut } from '../lib/types'

export function AdminResolvePage() {
  const { data: cases, loading, error, refetch } = useFetch<CaseSummaryOut[]>(() => api.get('/api/admin/cases'), [])
  const [busyCase, setBusyCase] = useState<string | null>(null)
  const [message, setMessage] = useState<string | null>(null)

  const markResolved = async (caseNumber: string) => {
    setBusyCase(caseNumber)
    setMessage(null)
    try {
      await api.post(`/api/admin/cases/${caseNumber}/mark-resolved`)
      setMessage(`${caseNumber} marked resolved. The citizen will now be asked to verify.`)
      refetch()
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Could not mark resolved.')
    } finally {
      setBusyCase(null)
    }
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-8">
      <p className="rounded-xl bg-accent-500/10 p-3 text-xs text-accent-600">
        Demo-only authority console — simulates a government official marking a case resolved. Not part of the citizen
        product and not linked from anywhere in the app.
      </p>
      <h1 className="mt-4 text-lg font-semibold text-ink-900">All cases</h1>

      {message && <p className="mt-2 rounded-xl bg-ink-100 p-3 text-sm text-ink-700">{message}</p>}
      {loading && <Spinner />}
      {error && <ErrorState message={error} onRetry={refetch} />}

      <div className="mt-4 flex flex-col gap-2">
        {cases?.map((c) => (
          <div key={c.case_number} className="flex items-center justify-between rounded-2xl bg-white p-4 shadow-sm ring-1 ring-ink-100">
            <div>
              <p className="font-medium text-ink-900">{c.issue_summary}</p>
              <p className="text-xs text-ink-500">
                {c.case_number} · {formatCategory(c.category)} · {formatStatus(c.status)}
                {c.is_overdue && ' · overdue'}
              </p>
            </div>
            <button
              onClick={() => markResolved(c.case_number)}
              disabled={busyCase === c.case_number || c.status === 'closed' || c.status === 'resolved_pending_verification'}
              className="rounded-full bg-ink-900 px-4 py-1.5 text-sm font-medium text-white disabled:opacity-40"
            >
              {c.status === 'resolved_pending_verification' ? 'Awaiting citizen' : c.status === 'closed' ? 'Closed' : 'Mark resolved'}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
