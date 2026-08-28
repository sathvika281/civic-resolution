import type { ReactNode } from 'react'
import { NavLink } from 'react-router-dom'
import { DisclaimerBanner } from './DisclaimerBanner'
import { TopBar } from './TopBar'

const tabClass = ({ isActive }: { isActive: boolean }) =>
  `flex flex-1 flex-col items-center gap-0.5 py-2 text-xs font-medium ${
    isActive ? 'text-brand-600' : 'text-ink-400'
  }`

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col bg-ink-50">
      <TopBar />
      <main className="mx-auto w-full max-w-2xl flex-1 px-4 pb-24 pt-4">{children}</main>
      <nav className="fixed inset-x-0 bottom-0 z-10 mx-auto flex w-full max-w-2xl border-t border-ink-100 bg-white/95 backdrop-blur">
        <NavLink to="/" end className={tabClass}>
          <span aria-hidden>🏠</span>
          Home
        </NavLink>
        <NavLink to="/community" className={tabClass}>
          <span aria-hidden>📍</span>
          Community
        </NavLink>
      </nav>
      <DisclaimerBanner />
    </div>
  )
}
