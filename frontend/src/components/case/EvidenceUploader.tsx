import { useState } from 'react'
import { api } from '../../lib/apiClient'
import type { CaseDetailOut } from '../../lib/types'

export function EvidenceUploader({ caseNumber, onUploaded }: { caseNumber: string; onUploaded: (updated: CaseDetailOut) => void }) {
  const [description, setDescription] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [open, setOpen] = useState(false)

  const submit = async () => {
    if (!description.trim()) return
    setSubmitting(true)
    try {
      const updated = await api.post<CaseDetailOut>(`/api/cases/${caseNumber}/evidence`, {
        uploaded_by: 'You',
        file_name: 'evidence_photo.jpg',
        description_text: description.trim(),
      })
      onUploaded(updated)
      setDescription('')
      setOpen(false)
    } finally {
      setSubmitting(false)
    }
  }

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="w-full rounded-2xl border border-dashed border-ink-300 py-3 text-sm font-medium text-ink-500 hover:border-brand-300 hover:text-brand-600"
      >
        📷 Add evidence (mock photo / document)
      </button>
    )
  }

  return (
    <div className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-ink-100">
      <p className="text-sm font-medium text-ink-800">Describe the evidence</p>
      <input
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="e.g. Photo of the pothole from the road side"
        className="mt-2 w-full rounded-xl border border-ink-200 bg-ink-50 p-2.5 text-sm outline-none focus:border-brand-400 focus:bg-white"
      />
      <div className="mt-3 flex gap-2">
        <button onClick={() => setOpen(false)} className="flex-1 rounded-full bg-ink-100 py-2 text-sm font-medium text-ink-700">
          Cancel
        </button>
        <button
          onClick={submit}
          disabled={submitting || !description.trim()}
          className="flex-1 rounded-full bg-brand-500 py-2 text-sm font-semibold text-white disabled:opacity-60"
        >
          {submitting ? 'Uploading…' : 'Upload'}
        </button>
      </div>
    </div>
  )
}
