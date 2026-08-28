import { useState } from 'react'
import { api } from '../../lib/apiClient'
import type { CaseDetailOut } from '../../lib/types'
import { Modal } from '../common/Modal'

interface Props {
  caseDetail: CaseDetailOut
  citizenId: string
  onClose: () => void
  onEscalated: () => void
}

export function EscalationModal({ caseDetail, citizenId, onClose, onEscalated }: Props) {
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [done, setDone] = useState(false)

  const submit = async () => {
    setSubmitting(true)
    setError(null)
    try {
      await api.post(`/api/cases/${caseDetail.case_number}/escalate`, { citizen_id: citizenId })
      setDone(true)
      onEscalated()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not submit the escalation.')
    } finally {
      setSubmitting(false)
    }
  }

  if (done) {
    return (
      <Modal onClose={onClose}>
        <p className="text-lg font-semibold text-ok-500">Escalation submitted successfully.</p>
        <p className="mt-2 text-sm text-ink-600">
          {caseDetail.authority.authority_name} has been notified with your case details and delay history.
        </p>
        <button onClick={onClose} className="mt-4 w-full rounded-full bg-brand-500 py-2.5 text-sm font-semibold text-white">
          Done
        </button>
      </Modal>
    )
  }

  return (
    <Modal onClose={onClose}>
      <p className="text-lg font-semibold text-ink-900">Escalate this case</p>
      <p className="mt-1 text-sm text-ink-500">This sends a structured escalation to the responsible authority. (Simulated — no real government system is contacted.)</p>

      <dl className="mt-4 space-y-2 rounded-2xl bg-ink-50 p-3 text-sm">
        <div className="flex justify-between"><dt className="text-ink-500">Case</dt><dd className="font-medium text-ink-800">{caseDetail.case_number}</dd></div>
        <div className="flex justify-between"><dt className="text-ink-500">Issue</dt><dd className="font-medium text-ink-800">{caseDetail.understanding.issue_summary}</dd></div>
        <div className="flex justify-between"><dt className="text-ink-500">Delay</dt><dd className="font-medium text-danger-600">{caseDetail.sla.days_overdue} days overdue</dd></div>
        <div className="flex justify-between"><dt className="text-ink-500">Sent to</dt><dd className="font-medium text-ink-800">{caseDetail.authority.authority_name}</dd></div>
      </dl>

      {error && <p className="mt-3 text-sm text-danger-600">{error}</p>}

      <div className="mt-4 flex gap-2">
        <button onClick={onClose} className="flex-1 rounded-full bg-ink-100 py-2.5 text-sm font-medium text-ink-700">
          Cancel
        </button>
        <button
          onClick={submit}
          disabled={submitting}
          className="flex-1 rounded-full bg-danger-500 py-2.5 text-sm font-semibold text-white disabled:opacity-60"
        >
          {submitting ? 'Submitting…' : 'Submit escalation'}
        </button>
      </div>
    </Modal>
  )
}
