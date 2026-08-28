export type ServiceCategory =
  | 'streetlight'
  | 'pothole'
  | 'water_supply'
  | 'pf_claim'
  | 'pension'
  | 'scholarship'
  | 'certificate'
  | 'other'

export type AuthorityType = 'municipal' | 'epfo' | 'education_dept' | 'pension_dept' | 'revenue_dept'

export type UrgencyLevel = 'low' | 'medium' | 'high'

export type CaseStatus = 'open' | 'in_progress' | 'resolved_pending_verification' | 'closed' | 'reopened'

export type StageStatus = 'completed' | 'current' | 'pending' | 'blocked'

export type AiSource = 'openai' | 'fallback'

export interface Citizen {
  id: string
  display_name: string
  persona_key: string
  phone: string | null
  created_at: string
}

export interface ProblemUnderstanding {
  issue_summary: string
  category: ServiceCategory
  location_text: string | null
  urgency: UrgencyLevel
  likely_required_evidence: string[]
  likely_next_action: string
  source: AiSource
}

export interface AuthorityResolution {
  authority_name: string
  authority_type: AuthorityType
  department: string
  jurisdiction_area: string
  responsible_role: string
  source: AiSource
}

export interface CaseExplanation {
  whats_happening: string
  current_blocker: string
  who_needs_to_act: string
  what_you_should_do: string
  next_step_label: string
  then_step_label: string
  source: AiSource
}

export interface CurrentResponsibilityOut {
  authority_name: string
  role: string
  jurisdiction_area: string
  days_at_current_stage: number
}

export interface TimelineEntryOut {
  stage_name: string
  status: StageStatus
  actor_name: string | null
  note: string | null
  occurred_at: string
}

export interface SlaOut {
  expected_days: number
  current_days: number
  is_overdue: boolean
  days_overdue: number
  note: string
}

export interface ClusterResult {
  possible_common_issue: boolean
  summary: string
  source: AiSource
}

export interface CommunityOut {
  affected_count: number
  confirmed_count: number
  cluster: ClusterResult | null
}

export interface EvidenceInterpretation {
  likely_shows: string
  missing_info_hint: string | null
  consistent_with_original_issue: boolean | null
  source: AiSource
}

export interface EvidenceOut {
  id: string
  file_name: string
  description_text: string | null
  interpretation: EvidenceInterpretation | null
  created_at: string
}

export interface RelatedCaseOut {
  case_number: string
  issue_summary: string
  location_text: string | null
  status: CaseStatus
}

export interface EscalationOut {
  id: string
  case_number: string
  reason_text: string
  escalated_to_authority_name: string
  status: string
  created_at: string
}

export interface CaseDetailOut {
  case_number: string
  status: CaseStatus
  understanding: ProblemUnderstanding
  authority: AuthorityResolution
  explanation: CaseExplanation
  current_responsibility: CurrentResponsibilityOut
  timeline: TimelineEntryOut[]
  sla: SlaOut
  community: CommunityOut
  evidence: EvidenceOut[]
  related_cases: RelatedCaseOut[]
  escalations: EscalationOut[]
  can_escalate: boolean
  awaiting_citizen_verification: boolean
}

export interface RedirectOut {
  redirected: true
  reason: string
  message: string
}

export interface CreateCaseResponse {
  redirected: boolean
  redirect: RedirectOut | null
  case: CaseDetailOut | null
}

export interface CaseSummaryOut {
  case_number: string
  issue_summary: string
  category: ServiceCategory
  status: CaseStatus
  is_overdue: boolean
  updated_at: string
}

export interface NearbyProblemOut {
  case_number: string
  issue_summary: string
  category: ServiceCategory
  location_text: string | null
  status: CaseStatus
  affected_count: number
  confirmed_count: number
  is_overdue: boolean
}

export interface HealthOut {
  status: string
  ai_mode: 'openai' | 'fallback'
  db_mode: 'supabase' | 'in_memory'
}
