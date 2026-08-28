import { Link } from 'react-router-dom'
import { useCitizen } from '../../context/CitizenContext'
import { clearStoredCitizenId } from '../../lib/identity'

export function TopBar() {
  const { citizen } = useCitizen()

  return (
    <header className="sticky top-0 z-10 flex items-center justify-between border-b border-ink-100 bg-white/90 px-4 py-3 backdrop-blur">
      <Link to="/" className="flex items-center gap-2">
        <span className="flex h-8 w-8 items-center justify-center rounded-xl bg-brand-500 text-sm font-bold text-white">
          CR
        </span>
        <span className="font-semibold text-ink-900">Civic Resolution</span>
      </Link>
      {citizen && (
        <button
          onClick={() => {
            clearStoredCitizenId()
            window.location.reload()
          }}
          className="flex items-center gap-2 rounded-full bg-ink-50 px-2.5 py-1.5 text-sm text-ink-600 hover:bg-ink-100"
          title="Switch demo persona"
        >
          <span className="flex h-6 w-6 items-center justify-center rounded-full bg-brand-100 text-xs font-semibold text-brand-700">
            {citizen.display_name.charAt(0)}
          </span>
          {citizen.display_name}
        </button>
      )}
    </header>
  )
}
