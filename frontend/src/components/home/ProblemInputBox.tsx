import { useState } from 'react'

interface Props {
  onSubmit: (rawText: string, locationText: string) => void
  submitting: boolean
  error: string | null
}

export function ProblemInputBox({ onSubmit, submitting, error }: Props) {
  const [text, setText] = useState('')
  const [location, setLocation] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!text.trim() || submitting) return
    onSubmit(text.trim(), location.trim())
  }

  return (
    <form onSubmit={handleSubmit} className="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-ink-100">
      <h1 className="text-xl font-semibold text-ink-900">What happened?</h1>
      <p className="mt-1 text-sm text-ink-500">
        Tell us what's wrong, in your own words. We'll figure out where it belongs.
      </p>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="e.g. The streetlight outside my house hasn't worked for two weeks."
        rows={3}
        className="mt-4 w-full resize-none rounded-2xl border border-ink-200 bg-ink-50 p-3 text-[15px] text-ink-900 outline-none focus:border-brand-400 focus:bg-white focus:ring-2 focus:ring-brand-100"
      />

      <input
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        placeholder="Location (optional) — e.g. Narapally, Hyderabad"
        className="mt-2 w-full rounded-2xl border border-ink-200 bg-ink-50 p-3 text-sm text-ink-900 outline-none focus:border-brand-400 focus:bg-white focus:ring-2 focus:ring-brand-100"
      />

      <div className="mt-3 flex items-center gap-2">
        <button
          type="button"
          disabled
          title="Voice input — coming soon"
          className="flex items-center gap-1.5 rounded-full bg-ink-50 px-3 py-2 text-sm text-ink-400"
        >
          🎙️ Tell us
        </button>
        <button
          type="button"
          disabled
          title="Attach evidence after your case is created"
          className="flex items-center gap-1.5 rounded-full bg-ink-50 px-3 py-2 text-sm text-ink-400"
        >
          📷 Add evidence
        </button>
        <button
          type="submit"
          disabled={!text.trim() || submitting}
          className="ml-auto rounded-full bg-brand-500 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-600 disabled:cursor-not-allowed disabled:bg-ink-200"
        >
          {submitting ? 'Understanding…' : 'Submit'}
        </button>
      </div>

      {error && <p className="mt-3 text-sm font-medium text-danger-600">{error}</p>}
    </form>
  )
}
