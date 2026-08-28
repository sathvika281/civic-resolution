import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { api } from '../lib/apiClient'
import { getStoredCitizenId, setStoredCitizenId } from '../lib/identity'
import type { Citizen } from '../lib/types'

interface CitizenContextValue {
  citizen: Citizen | null
  citizens: Citizen[]
  loading: boolean
  selectCitizen: (citizenId: string) => void
}

const CitizenContext = createContext<CitizenContextValue | undefined>(undefined)

export function CitizenProvider({ children }: { children: ReactNode }) {
  const [citizens, setCitizens] = useState<Citizen[]>([])
  const [citizen, setCitizen] = useState<Citizen | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    api
      .get<Citizen[]>('/api/citizens')
      .then((list) => {
        if (cancelled) return
        setCitizens(list)
        const storedId = getStoredCitizenId()
        const match = list.find((c) => c.id === storedId)
        if (match) setCitizen(match)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [])

  const selectCitizen = (citizenId: string) => {
    const match = citizens.find((c) => c.id === citizenId)
    if (match) {
      setCitizen(match)
      setStoredCitizenId(match.id)
    }
  }

  return (
    <CitizenContext.Provider value={{ citizen, citizens, loading, selectCitizen }}>
      {children}
    </CitizenContext.Provider>
  )
}

export function useCitizen(): CitizenContextValue {
  const ctx = useContext(CitizenContext)
  if (!ctx) throw new Error('useCitizen must be used within CitizenProvider')
  return ctx
}
