export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

export function formatDaysAgo(iso: string): string {
  const days = Math.floor((Date.now() - new Date(iso).getTime()) / (1000 * 60 * 60 * 24))
  if (days <= 0) return 'today'
  if (days === 1) return '1 day ago'
  return `${days} days ago`
}

const CATEGORY_LABELS: Record<string, string> = {
  streetlight: 'Streetlight',
  pothole: 'Road / Pothole',
  water_supply: 'Water Supply',
  pf_claim: 'PF Claim',
  pension: 'Pension',
  scholarship: 'Scholarship',
  certificate: 'Certificate',
  other: 'General Issue',
}

export function formatCategory(category: string): string {
  return CATEGORY_LABELS[category] ?? category
}

const STATUS_LABELS: Record<string, string> = {
  open: 'Open',
  in_progress: 'In Progress',
  resolved_pending_verification: 'Awaiting Your Confirmation',
  closed: 'Closed',
  reopened: 'Reopened',
}

export function formatStatus(status: string): string {
  return STATUS_LABELS[status] ?? status
}
