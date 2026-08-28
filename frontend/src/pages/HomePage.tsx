import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { RedirectNotice } from '../components/common/RedirectNotice'
import { ErrorState } from '../components/common/EmptyState'
import { Spinner } from '../components/common/Spinner'
import { NearbyProblemsList } from '../components/home/NearbyProblemsList'
import { ProblemInputBox } from '../components/home/ProblemInputBox'
import { RecentCasesList } from '../components/home/RecentCasesList'
import { useCitizen } from '../context/CitizenContext'
import { useCases } from '../hooks/useCases'
import { useCommunityFeed } from '../hooks/useCommunityFeed'
import { api, ApiError } from '../lib/apiClient'
import type { CreateCaseResponse } from '../lib/types'

export function HomePage() {
  const { citizen } = useCitizen()
  const navigate = useNavigate()
  const cases = useCases(citizen?.id)
  const nearby = useCommunityFeed(citizen?.id)

  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [redirectMessage, setRedirectMessage] = useState<string | null>(null)

  const handleSubmit = async (rawText: string, locationText: string) => {
    if (!citizen) return
    setSubmitting(true)
    setError(null)
    setRedirectMessage(null)
    try {
      const response = await api.post<CreateCaseResponse>('/api/cases', {
        citizen_id: citizen.id,
        raw_text: rawText,
        location_text: locationText || null,
      })
      if (response.redirected && response.redirect) {
        setRedirectMessage(response.redirect.message)
        return
      }
      if (response.case) {
        navigate(`/case/${response.case.case_number}`)
      }
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not submit your problem. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <ProblemInputBox onSubmit={handleSubmit} submitting={submitting} error={error} />

      {redirectMessage && <RedirectNotice message={redirectMessage} onDismiss={() => setRedirectMessage(null)} />}

      <section>
        <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-ink-500">Recent cases</h2>
        {cases.loading && <Spinner label="Loading your cases…" />}
        {cases.error && <ErrorState message={cases.error} onRetry={cases.refetch} />}
        {cases.data && <RecentCasesList cases={cases.data} />}
      </section>

      <section>
        <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-ink-500">Problems near you</h2>
        {nearby.loading && <Spinner label="Loading nearby reports…" />}
        {nearby.error && <ErrorState message={nearby.error} onRetry={nearby.refetch} />}
        {nearby.data && <NearbyProblemsList problems={nearby.data} />}
      </section>
    </div>
  )
}
