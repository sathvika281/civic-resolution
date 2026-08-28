export function EscalateButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="w-full rounded-2xl bg-danger-500 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-danger-600"
    >
      This case appears overdue — Escalate
    </button>
  )
}
