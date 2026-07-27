import { useState, useEffect } from 'react'
import IntakePanel from './components/IntakePanel'
import CandidateCard from './components/CandidateCard'
import { getCandidates, deleteCandidate } from './api'
import ChatPanel from './components/ChatPanel'

function App() {
  const [results, setResults] = useState(null)
  const [candidateCount, setCandidateCount] = useState(0)
  const [loadingCandidates, setLoadingCandidates] = useState(true)

  const refreshCandidateCount = async () => {
    try {
      const res = await getCandidates()
      setCandidateCount(res.data.count)
    } catch (err) {
      console.error('Could not reach backend:', err)
    } finally {
      setLoadingCandidates(false)
    }
  }

  const handleDeleteCandidate = async (fileName) => {
    try {
      await deleteCandidate(fileName)
      refreshCandidateCount()
      setResults((prev) => (prev ? prev.filter((c) => c.file_name !== fileName) : prev))
    } catch (err) {
      console.error('Delete failed:', err)
    }
  }

  useEffect(() => {
    refreshCandidateCount()
  }, [])

  return (
    <div className="min-h-screen bg-ink">
      {/* Header */}
      <header className="border-b border-hairline">
        <div className="max-w-6xl mx-auto px-6 py-6 flex items-baseline gap-3">
          <h1 className="font-display text-3xl text-text-primary">Docket</h1>
          <p className="font-mono text-xs text-text-muted uppercase tracking-widest">
            AI Resume Screening
          </p>
        </div>
      </header>

      {/* Main layout */}
      <main className="max-w-6xl mx-auto px-6 py-10 grid lg:grid-cols-[380px_1fr] gap-8">
        {/* Left: intake panel, sticky on desktop */}
        <div className="lg:sticky lg:top-10 lg:self-start">
          <IntakePanel
            onScreenResults={setResults}
            candidateCount={candidateCount}
            onCandidatesUpdated={refreshCandidateCount}
          />
        </div>

        {/* Right: results */}
        <div>
          {results === null && (
            <div className="border border-dashed border-hairline rounded-sm p-12 text-center">
              <p className="font-display text-xl text-text-muted mb-2">
                No screening run yet
              </p>
              <p className="text-sm text-text-muted">
                {loadingCandidates
                  ? 'Checking for candidates on file...'
                  : candidateCount > 0
                  ? `${candidateCount} candidate${candidateCount !== 1 ? 's are' : ' is'} on file. Enter a job description and click Screen Candidates.`
                  : 'Upload resumes on the left, then enter a job description to screen candidates.'}
              </p>
            </div>
          )}

          {results !== null && results.length === 0 && (
            <p className="text-text-muted text-center py-12">No candidates were screened.</p>
          )}

          {results !== null && results.length > 0 && (
            <div className="space-y-3">
              <p className="font-mono text-xs text-text-muted uppercase tracking-wider mb-4">
                {results.length} candidate{results.length !== 1 ? 's' : ''} ranked
              </p>
              {results.map((candidate, i) => (
                <CandidateCard
                  key={candidate.file_name}
                  candidate={candidate}
                  rank={i + 1}
                  onDelete={handleDeleteCandidate}
                />
              ))}
            </div>
          )}

          <div className="mt-8">
            <ChatPanel candidateCount={candidateCount} />
          </div>
        </div>
      </main>
    </div>
  )
}

export default App