import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { CaseHeader } from '../components/case/CaseHeader'
import { CommunityConfirmBar } from '../components/case/CommunityConfirmBar'
import { CurrentResponsibilityCard } from '../components/case/CurrentResponsibilityCard'
import { EscalateButton } from '../components/case/EscalateButton'
import { EscalationModal } from '../components/case/EscalationModal'
import { EvidenceList } from '../components/case/EvidenceList'
import { EvidenceUploader } from '../components/case/EvidenceUploader'
import { RelatedCasesList } from '../components/case/RelatedCasesList'
import { SlaDelayBadge } from '../components/case/SlaDelayBadge'
import { TimelineView } from '../components/case/TimelineView'
import { UnderstandingSummary } from '../components/case/UnderstandingSummary'
import { VerifyResolutionModal } from '../components/case/VerifyResolutionModal'
import { WhatsHappeningCard } from '../components/case/WhatsHappeningCard'
import { WhatYouShouldDoCard } from '../components/case/WhatYouShouldDoCard'
import { ErrorState } from '../components/common/EmptyState'
import { Spinner } from '../components/common/Spinner'
import { useCitizen } from '../context/CitizenContext'
import { useCase } from '../hooks/useCase'

export function CaseDetailPage() {
  const { caseNumber } = useParams<{ caseNumber: string }>()
  const { citizen } = useCitizen()
  const { data: caseDetail, loading, error, refetch } = useCase(caseNumber)
  const [showEscalation, setShowEscalation] = useState(false)
  const [showVerification, setShowVerification] = useState(false)

  if (loading && !caseDetail) return <Spinner label="Loading case…" />
  if (error && !caseDetail) return <ErrorState message={error} onRetry={refetch} />
  if (!caseDetail || !citizen) return null

  return (
    <div className="flex flex-col gap-4">
      <CaseHeader issueSummary={caseDetail.understanding.issue_summary} caseNumber={caseDetail.case_number} status={caseDetail.status} />

      {caseDetail.awaiting_citizen_verification && (
        <button
          onClick={() => setShowVerification(true)}
          className="w-full rounded-2xl bg-brand-500 py-3 text-sm font-semibold text-white shadow-sm"
        >
          The authority marked this resolved — Is it actually fixed?
        </button>
      )}

      <UnderstandingSummary understanding={caseDetail.understanding} />
      <CurrentResponsibilityCard responsibility={caseDetail.current_responsibility} />
      <WhatsHappeningCard explanation={caseDetail.explanation} />
      <WhatYouShouldDoCard explanation={caseDetail.explanation} />
      <TimelineView timeline={caseDetail.timeline} />
      <SlaDelayBadge sla={caseDetail.sla} />

      {caseDetail.can_escalate && !caseDetail.awaiting_citizen_verification && (
        <EscalateButton onClick={() => setShowEscalation(true)} />
      )}

      <CommunityConfirmBar
        caseNumber={caseDetail.case_number}
        citizenId={citizen.id}
        community={caseDetail.community}
        onConfirmed={refetch}
      />

      <EvidenceList evidence={caseDetail.evidence} />
      <EvidenceUploader caseNumber={caseDetail.case_number} onUploaded={refetch} />
      <RelatedCasesList relatedCases={caseDetail.related_cases} />

      {showEscalation && (
        <EscalationModal
          caseDetail={caseDetail}
          citizenId={citizen.id}
          onClose={() => setShowEscalation(false)}
          onEscalated={refetch}
        />
      )}
      {showVerification && (
        <VerifyResolutionModal
          caseDetail={caseDetail}
          citizenId={citizen.id}
          onClose={() => setShowVerification(false)}
          onVerified={refetch}
        />
      )}
    </div>
  )
}
