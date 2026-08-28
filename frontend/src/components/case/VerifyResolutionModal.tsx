import { useState } from 'react'
import { api } from '../../lib/apiClient'
import type { CaseDetailOut } from '../../lib/types'
import { Modal } from '../common/Modal'

interface Props {
  caseDetail: CaseDetailOut
  citizenId: string
  onClose: () => void
  onVerified: (updated: CaseDetailOut) => void
}

type Step = 'ask' | 'explain' | 'reopened' | 'closed'

export function VerifyResolutionModal({ caseDetail, citizenId, onClose, onVerified }: Props) {
  const [step, setStep] = useState<Step>('ask')
  const [explanation, setExplanation] = useState('')
  const [evidenceDescription, setEvidenceDescription] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [aiComment, setAiComment] = useState<string | null>(null)

  const confirmFixed = async () => {
    setSubmitting(true)
    setError(null)
    try {
      const updated = await api.post<CaseDetailOut>(`/api/cases/${caseDetail.case_number}/verify`, {
        citizen_id: citizenId,
        is_actually_fixed: true,
      })
      onVerified(updated)
      setStep('closed')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not record your confirmation.')
    } finally {
      setSubmitting(false)
    }
  }

  const submitStillBroken = async () => {
    setSubmitting(true)
    setError(null)
    try {
      let latest = caseDetail
      if (evidenceDescription.trim()) {
        latest = await api.post<CaseDetailOut>(`/api/cases/${caseDetail.case_number}/evidence`, {
          uploaded_by: 'You',
          file_name: 'updated_evidence.jpg',
          description_text: evidenceDescription.trim(),
          stage_context: 'resolution_verification',
        })
      }
      const updated = await api.post<CaseDetailOut>(`/api/cases/${caseDetail.case_number}/verify`, {
        citizen_id: citizenId,
        is_actually_fixed: false,
        explanation_text: explanation.trim() || undefined,
      })
      const lastEvidence = latest.evidence[latest.evidence.length - 1]
      setAiComment(
        lastEvidence?.interpretation?.likely_shows ??
          'The issue you reported does not appear to be resolved based on your explanation.',
      )
      onVerified(updated)
      setStep('reopened')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not reopen the case.')
    } finally {
      setSubmitting(false)
    }
  }

  if (step === 'closed') {
    return (
      <Modal onClose={onClose}>
        <p className="text-lg font-semibold text-ok-500">Great — case closed.</p>
        <p className="mt-2 text-sm text-ink-600">Thanks for confirming. We're glad this got sorted out.</p>
        <button onClick={onClose} className="mt-4 w-full rounded-full bg-brand-500 py-2.5 text-sm font-semibold text-white">
          Done
        </button>
      </Modal>
    )
  }

  if (step === 'reopened') {
    return (
      <Modal onClose={onClose}>
        <p className="text-lg font-semibold text-danger-600">Case reopened</p>
        {aiComment && (
          <p className="mt-2 rounded-xl bg-ink-50 p-3 text-sm text-ink-700">
            AI note: {aiComment} (Not a legal or final determination.)
          </p>
        )}
        <p className="mt-2 text-sm text-ink-600">
          We've sent this back to {caseDetail.authority.authority_name} with your update.
        </p>
        <button onClick={onClose} className="mt-4 w-full rounded-full bg-brand-500 py-2.5 text-sm font-semibold text-white">
          Done
        </button>
      </Modal>
    )
  }

  if (step === 'explain') {
    return (
      <Modal onClose={onClose}>
        <p className="text-lg font-semibold text-ink-900">Tell us what's still wrong</p>
        <textarea
          value={explanation}
          onChange={(e) => setExplanation(e.target.value)}
          placeholder="e.g. The streetlight is still off at night."
          rows={2}
          className="mt-3 w-full resize-none rounded-2xl border border-ink-200 bg-ink-50 p-3 text-sm outline-none focus:border-brand-400 focus:bg-white"
        />
        <input
          value={evidenceDescription}
          onChange={(e) => setEvidenceDescription(e.target.value)}
          placeholder="Describe new evidence (mock photo/document) — optional"
          className="mt-2 w-full rounded-2xl border border-ink-200 bg-ink-50 p-3 text-sm outline-none focus:border-brand-400 focus:bg-white"
        />
        {error && <p className="mt-2 text-sm text-danger-600">{error}</p>}
        <div className="mt-4 flex gap-2">
          <button onClick={() => setStep('ask')} className="flex-1 rounded-full bg-ink-100 py-2.5 text-sm font-medium text-ink-700">
            Back
          </button>
          <button
            onClick={submitStillBroken}
            disabled={submitting}
            className="flex-1 rounded-full bg-danger-500 py-2.5 text-sm font-semibold text-white disabled:opacity-60"
          >
            {submitting ? 'Sending…' : 'Reopen case'}
          </button>
        </div>
      </Modal>
    )
  }

  return (
    <Modal onClose={onClose}>
      <p className="text-lg font-semibold text-ink-900">Is it actually fixed?</p>
      <p className="mt-1 text-sm text-ink-500">
        {caseDetail.authority.authority_name} marked this case resolved. We want to hear it from you before we close it.
      </p>
      {error && <p className="mt-2 text-sm text-danger-600">{error}</p>}
      <div className="mt-4 flex gap-2">
        <button
          onClick={() => setStep('explain')}
          className="flex-1 rounded-full bg-ink-100 py-2.5 text-sm font-semibold text-ink-700"
        >
          ❌ No, still happening
        </button>
        <button
          onClick={confirmFixed}
          disabled={submitting}
          className="flex-1 rounded-full bg-ok-500 py-2.5 text-sm font-semibold text-white disabled:opacity-60"
        >
          ✅ Yes, resolved
        </button>
      </div>
    </Modal>
  )
}
