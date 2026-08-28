import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-2 text-center">
      <p className="text-lg font-semibold text-ink-900">Page not found</p>
      <Link to="/" className="text-brand-600 underline">
        Go back home
      </Link>
    </div>
  )
}
