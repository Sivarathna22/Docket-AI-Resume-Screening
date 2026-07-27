import { useState } from 'react'

const verdictStyles = {
  'Strong Match': {
    color: 'text-stamp-strong',
    border: 'border-stamp-strong',
    label: 'STRONG MATCH',
  },
  'Possible Match': {
    color: 'text-stamp-possible',
    border: 'border-stamp-possible',
    label: 'POSSIBLE MATCH',
  },
  'Weak Match': {
    color: 'text-stamp-weak',
    border: 'border-stamp-weak',
    label: 'WEAK MATCH',
  },
  'Error': {
    color: 'text-text-muted',
    border: 'border-text-muted',
    label: 'PARSE ERROR',
  },
}

function CandidateCard({ candidate, rank, onDelete }) {
  const [expanded, setExpanded] = useState(false)
  const style = verdictStyles[candidate.verdict] || verdictStyles['Error']

  const displayName = candidate.file_name
    .replace('.pdf', '')
    .replace(/_/g, ' ')

  return (
    <div className="bg-panel border border-hairline rounded-sm overflow-hidden">
      <div
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-4 p-5 text-left hover:bg-panel-light transition-colors cursor-pointer"
      >
        {/* Case number */}
        <div className="font-mono text-text-muted text-sm w-8 shrink-0">
          {String(rank).padStart(2, '0')}
        </div>

        {/* Name + score */}
        <div className="flex-1 min-w-0">
          <h3 className="font-display text-lg text-text-primary capitalize truncate">
            {displayName}
          </h3>
          <div className="flex items-center gap-2 mt-1">
            <span className="font-mono text-2xl text-accent">
              {candidate.match_score ?? '--'}
            </span>
            <span className="font-mono text-xs text-text-muted">/100</span>
          </div>
        </div>

        {/* Stamp */}
        <div
          className={`font-stamp text-xs sm:text-sm px-3 py-1.5 border-2 rounded-sm rotate-[-6deg] ${style.color} ${style.border} shrink-0`}
          style={{ letterSpacing: '0.05em' }}
        >
          {style.label}
        </div>

        {/* Delete button */}
        {onDelete && (
          <span
            onClick={(e) => {
              e.stopPropagation()
              if (window.confirm(`Remove ${displayName} from the candidate pool?`)) {
                onDelete(candidate.file_name)
              }
            }}
            className="text-text-muted hover:text-stamp-weak shrink-0 cursor-pointer text-lg px-1"
            title="Remove candidate"
          >
            ✕
          </span>
        )}
      </div>

      {expanded && (
        <div className="px-5 pb-5 pt-1 border-t border-hairline">
          <div className="grid sm:grid-cols-2 gap-4 mt-3">
            <div>
              <p className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2">
                Strengths
              </p>
              <ul className="space-y-1">
                {(candidate.strengths || []).map((s, i) => (
                  <li key={i} className="text-sm text-text-primary flex gap-2">
                    <span className="text-stamp-strong">+</span> {s}
                  </li>
                ))}
                {(!candidate.strengths || candidate.strengths.length === 0) && (
                  <li className="text-sm text-text-muted italic">None identified</li>
                )}
              </ul>
            </div>
            <div>
              <p className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2">
                Gaps
              </p>
              <ul className="space-y-1">
                {(candidate.gaps || []).map((g, i) => (
                  <li key={i} className="text-sm text-text-primary flex gap-2">
                    <span className="text-stamp-weak">-</span> {g}
                  </li>
                ))}
                {(!candidate.gaps || candidate.gaps.length === 0) && (
                  <li className="text-sm text-text-muted italic">None identified</li>
                )}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default CandidateCard