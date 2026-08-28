import { useCitizen } from '../../context/CitizenContext'

export function PersonaPicker() {
  const { citizens, selectCitizen, loading } = useCitizen()

  if (loading) return null

  return (
    <div className="flex min-h-screen items-center justify-center bg-ink-50 px-4">
      <div className="w-full max-w-sm rounded-3xl bg-white p-6 shadow-sm ring-1 ring-ink-100">
        <h1 className="text-lg font-semibold text-ink-900">Who's using this demo?</h1>
        <p className="mt-1 text-sm text-ink-500">
          This prototype uses mock citizen identities instead of real login. Pick one to continue.
        </p>
        <div className="mt-5 flex flex-col gap-2">
          {citizens.map((c) => (
            <button
              key={c.id}
              onClick={() => selectCitizen(c.id)}
              className="flex items-center gap-3 rounded-2xl border border-ink-100 px-4 py-3 text-left transition hover:border-brand-300 hover:bg-brand-50"
            >
              <span className="flex h-9 w-9 items-center justify-center rounded-full bg-brand-100 text-sm font-semibold text-brand-700">
                {c.display_name.charAt(0)}
              </span>
              <span className="font-medium text-ink-800">{c.display_name}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
