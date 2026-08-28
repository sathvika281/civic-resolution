export function RedirectNotice({ message, onDismiss }: { message: string; onDismiss: () => void }) {
  return (
    <div className="rounded-2xl border border-accent-500/30 bg-accent-500/10 p-4">
      <p className="text-sm font-medium text-ink-800">{message}</p>
      <button
        onClick={onDismiss}
        className="mt-3 rounded-full bg-white px-4 py-1.5 text-sm font-medium text-ink-700 shadow-sm ring-1 ring-ink-200 hover:bg-ink-50"
      >
        Okay, let me rephrase
      </button>
    </div>
  )
}
