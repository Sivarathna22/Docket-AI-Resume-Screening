import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})

export const uploadResumes = (files) => {
  const formData = new FormData()
  files.forEach((file) => formData.append('files', file))
  return api.post('/upload-resumes', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const getCandidates = () => api.get('/candidates')

export const screenCandidates = (jobDescription) =>
  api.post('/screen', { job_description: jobDescription })

export const deleteCandidate = (fileName) =>
  api.delete(`/candidates/${encodeURIComponent(fileName)}`)

export const chatQuery = (question) =>
  api.post('/chat', { question })

export default api