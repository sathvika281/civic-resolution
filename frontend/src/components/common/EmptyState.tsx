export function EmptyState({ title, description }: { title: string; description?: string }) {
  return (
    <div className="rounded-2xl border border-dashed border-ink-200 bg-white/60 px-5 py-8 text-center">
      <p className="font-medium text-ink-700">{title}</p>
      {description && <p className="mt-1 text-sm text-ink-500">{description}</p>}
    </div>
  )
}

export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="rounded-2xl border border-danger-500/30 bg-danger-500/5 px-5 py-6 text-center">
      <p className="font-medium text-danger-600">Something went wrong</p>
      <p className="mt-1 text-sm text-ink-500">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-3 rounded-full bg-white px-4 py-1.5 text-sm font-medium text-ink-700 shadow-sm ring-1 ring-ink-200 hover:bg-ink-50"
        >
          Try again
        </button>
      )}
    </div>
  )
}
