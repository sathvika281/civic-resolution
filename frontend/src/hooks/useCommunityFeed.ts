import { api } from '../lib/apiClient'
import type { NearbyProblemOut } from '../lib/types'
import { useFetch } from './useFetch'

export function useCommunityFeed(excludeCitizenId: string | undefined) {
  return useFetch<NearbyProblemOut[]>(
    () => api.get<NearbyProblemOut[]>(`/api/community/nearby${excludeCitizenId ? `?exclude_citizen_id=${encodeURIComponent(excludeCitizenId)}` : ''}`),
    [excludeCitizenId],
  )
}
