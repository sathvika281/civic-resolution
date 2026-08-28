import { ErrorState } from '../components/common/EmptyState'
import { Spinner } from '../components/common/Spinner'
import { NearbyProblemsList } from '../components/home/NearbyProblemsList'
import { useCitizen } from '../context/CitizenContext'
import { useCommunityFeed } from '../hooks/useCommunityFeed'

export function CommunityPage() {
  const { citizen } = useCitizen()
  const nearby = useCommunityFeed(citizen?.id)

  return (
    <div>
      <h1 className="text-xl font-semibold text-ink-900">Problems near you</h1>
      <p className="mt-1 text-sm text-ink-500">Civic issues reported by other citizens in this prototype's demo data.</p>
      <div className="mt-4">
        {nearby.loading && <Spinner label="Loading nearby reports…" />}
        {nearby.error && <ErrorState message={nearby.error} onRetry={nearby.refetch} />}
        {nearby.data && <NearbyProblemsList problems={nearby.data} />}
      </div>
    </div>
  )
}
