import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import { AppShell } from './components/layout/AppShell'
import { PersonaPicker } from './components/common/PersonaPicker'
import { Spinner } from './components/common/Spinner'
import { CitizenProvider, useCitizen } from './context/CitizenContext'
import { AdminResolvePage } from './pages/AdminResolvePage'
import { CaseDetailPage } from './pages/CaseDetailPage'
import { CommunityPage } from './pages/CommunityPage'
import { HomePage } from './pages/HomePage'
import { NotFoundPage } from './pages/NotFoundPage'

function CitizenApp() {
  const { citizen, loading } = useCitizen()

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Spinner label="Loading Civic Resolution…" />
      </div>
    )
  }

  if (!citizen) {
    return <PersonaPicker />
  }

  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/case/:caseNumber" element={<CaseDetailPage />} />
        <Route path="/community" element={<CommunityPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </AppShell>
  )
}

export default function App() {
  return (
    <Router>
      <CitizenProvider>
        <Routes>
          <Route path="/admin/*" element={<AdminResolvePage />} />
          <Route path="/*" element={<CitizenApp />} />
        </Routes>
      </CitizenProvider>
    </Router>
  )
}
