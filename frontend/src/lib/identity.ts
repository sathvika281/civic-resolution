const STORAGE_KEY = 'civic_resolution_citizen_id'

export function getStoredCitizenId(): string | null {
  try {
    return localStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}

export function setStoredCitizenId(citizenId: string): void {
  try {
    localStorage.setItem(STORAGE_KEY, citizenId)
  } catch {
    // localStorage unavailable (private browsing, etc.) — identity just won't persist
  }
}

export function clearStoredCitizenId(): void {
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch {
    // ignore
  }
}
