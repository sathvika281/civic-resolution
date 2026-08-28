import { api } from '../lib/apiClient'
import type { CaseSummaryOut } from '../lib/types'
import { useFetch } from './useFetch'

export function useCases(citizenId: string | undefined) {
  return useFetch<CaseSummaryOut[]>(
    () => (citizenId ? api.get<CaseSummaryOut[]>(`/api/cases?citizen_id=${encodeURIComponent(citizenId)}`) : Promise.resolve([])),
    [citizenId],
  )
}
