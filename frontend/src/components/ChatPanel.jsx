import { useState, useRef, useEffect } from 'react'
import { chatQuery } from '../api'

function ChatPanel({ candidateCount }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const scrollRef = useRef(null)

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleAsk = async () => {
    const question = input.trim()
    if (!question || loading) return

    setMessages((prev) => [...prev, { role: 'user', text: question }])
    setInput('')
    setLoading(true)

    try {
      const res = await chatQuery(question)
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: res.data.answer, sources: res.data.sources },
      ])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: 'Something went wrong reaching the backend.', error: true },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleAsk()
    }
  }

  return (
    <div className="bg-panel border border-hairline rounded-sm flex flex-col h-[500px]">
      <div className="p-4 border-b border-hairline">
        <h2 className="font-display text-lg text-text-primary">Ask the Pool</h2>
        <p className="text-xs text-text-muted font-mono mt-0.5">
          {candidateCount} candidate{candidateCount !== 1 ? 's' : ''} searchable
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <p className="text-sm text-text-muted italic">
            Try: "Who has AWS experience?" or "Which candidates have led a team?"
          </p>
        )}

        {messages.map((m, i) => (
          <div key={i} className={m.role === 'user' ? 'text-right' : 'text-left'}>
            <div
              className={`inline-block max-w-[85%] px-4 py-2 rounded-sm text-sm text-left ${
                m.role === 'user'
                  ? 'bg-accent text-ink'
                  : m.error
                  ? 'bg-ink border border-stamp-weak text-stamp-weak'
                  : 'bg-ink border border-hairline text-text-primary'
              }`}
            >
              {m.text}
              {m.sources && m.sources.length > 0 && (
                <div className="mt-2 pt-2 border-t border-hairline flex flex-wrap gap-1">
                  {[...new Set(m.sources.map((s) => s.file_name))].map((f) => (
                    <span
                      key={f}
                      className="font-mono text-[10px] text-text-muted bg-panel-light px-2 py-0.5 rounded-sm"
                    >
                      {f.replace('.pdf', '')}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="text-left">
            <div className="inline-block bg-ink border border-hairline px-4 py-2 rounded-sm text-sm text-text-muted">
              Thinking...
            </div>
          </div>
        )}

        <div ref={scrollRef} />
      </div>

      <div className="p-4 border-t border-hairline flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about the candidates..."
          className="flex-1 bg-ink border border-hairline rounded-sm px-3 py-2 text-sm text-text-primary placeholder-text-muted focus:outline-none focus:border-accent"
        />
        <button
          onClick={handleAsk}
          disabled={loading}
          className="bg-accent text-ink font-medium px-4 py-2 rounded-sm hover:bg-accent-soft disabled:opacity-50 transition-colors"
        >
          Ask
        </button>
      </div>
    </div>
  )
}

export default ChatPanel