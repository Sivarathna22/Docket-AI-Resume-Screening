import { useState, useRef } from 'react'
import { uploadResumes, screenCandidates } from '../api'

function IntakePanel({ onScreenResults, candidateCount, onCandidatesUpdated }) {
  const [jobDescription, setJobDescription] = useState('')
  const [files, setFiles] = useState([])
  const [uploading, setUploading] = useState(false)
  const [screening, setScreening] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const [error, setError] = useState('')
  const fileInputRef = useRef(null)

  const handleFiles = (fileList) => {
    const pdfFiles = Array.from(fileList).filter((f) =>
      f.name.toLowerCase().endsWith('.pdf')
    )
    setFiles((prev) => [...prev, ...pdfFiles])
    setError('')
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragActive(false)
    handleFiles(e.dataTransfer.files)
  }

  const removeFile = (index) => {
    setFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleUpload = async () => {
    if (files.length === 0) return
    setUploading(true)
    setError('')
    try {
      await uploadResumes(files)
      setFiles([])
      onCandidatesUpdated()
    } catch (err) {
      setError('Upload failed. Is the backend running on port 8000?')
    } finally {
      setUploading(false)
    }
  }

  const handleScreen = async () => {
    if (!jobDescription.trim()) {
      setError('Enter a job description first.')
      return
    }
    if (candidateCount === 0) {
      setError('Upload at least one resume before screening.')
      return
    }
    setScreening(true)
    setError('')
    try {
      const res = await screenCandidates(jobDescription)
      onScreenResults(res.data.results)
    } catch (err) {
      setError('Screening failed. Check the backend terminal for errors.')
    } finally {
      setScreening(false)
    }
  }

  return (
    <div className="bg-panel border border-hairline rounded-sm p-6 space-y-6">
      <div>
        <h2 className="font-display text-xl text-text-primary mb-1">Intake</h2>
        <p className="text-sm text-text-muted">
          {candidateCount} candidate{candidateCount !== 1 ? 's' : ''} on file
        </p>
      </div>

      {/* Job description */}
      <div>
        <label className="font-mono text-xs text-text-muted uppercase tracking-wider block mb-2">
          Job Description
        </label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the role requirements here..."
          rows={6}
          className="w-full bg-ink border border-hairline rounded-sm p-3 text-sm text-text-primary placeholder-text-muted focus:outline-none focus:border-accent resize-none"
        />
      </div>

      {/* Upload zone */}
      <div>
        <label className="font-mono text-xs text-text-muted uppercase tracking-wider block mb-2">
          Upload Resumes
        </label>
        <div
          onDragOver={(e) => { e.preventDefault(); setDragActive(true) }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-sm p-6 text-center cursor-pointer transition-colors ${
            dragActive ? 'border-accent bg-panel-light' : 'border-hairline hover:border-text-muted'
          }`}
        >
          <p className="text-sm text-text-muted">
            Drag PDFs here, or click to browse
          </p>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            multiple
            className="hidden"
            onChange={(e) => handleFiles(e.target.files)}
          />
        </div>

        {files.length > 0 && (
          <ul className="mt-3 space-y-1">
            {files.map((f, i) => (
              <li key={i} className="flex items-center justify-between text-sm text-text-primary bg-ink px-3 py-2 rounded-sm">
                <span className="truncate">{f.name}</span>
                <button
                  onClick={() => removeFile(i)}
                  className="text-text-muted hover:text-stamp-weak ml-2 shrink-0"
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
        )}

        {files.length > 0 && (
          <button
            onClick={handleUpload}
            disabled={uploading}
            className="mt-3 w-full bg-accent text-ink font-medium py-2 rounded-sm hover:bg-accent-soft disabled:opacity-50 transition-colors"
          >
            {uploading ? 'Indexing...' : `Upload & Index ${files.length} file${files.length !== 1 ? 's' : ''}`}
          </button>
        )}
      </div>

      {error && (
        <p className="text-sm text-stamp-weak border border-stamp-weak rounded-sm p-2">
          {error}
        </p>
      )}

      <button
        onClick={handleScreen}
        disabled={screening}
        className="w-full bg-transparent border-2 border-accent text-accent font-display text-lg py-3 rounded-sm hover:bg-accent hover:text-ink disabled:opacity-50 transition-colors"
      >
        {screening ? 'Screening candidates...' : 'Screen Candidates'}
      </button>
    </div>
  )
}

export default IntakePanel