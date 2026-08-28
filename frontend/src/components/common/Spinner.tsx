export function Spinner({ label = 'Loading…' }: { label?: string }) {
  return (
    <div className="flex items-center gap-2 py-6 text-ink-500 text-sm">
      <span className="h-4 w-4 animate-spin rounded-full border-2 border-ink-300 border-t-brand-500" />
      {label}
    </div>
  )
}
