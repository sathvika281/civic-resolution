import { api } from '../lib/apiClient'
import type { CaseDetailOut } from '../lib/types'
import { useFetch } from './useFetch'

export function useCase(caseNumber: string | undefined) {
  return useFetch<CaseDetailOut>(
    () => api.get<CaseDetailOut>(`/api/cases/${encodeURIComponent(caseNumber ?? '')}`),
    [caseNumber],
  )
}
