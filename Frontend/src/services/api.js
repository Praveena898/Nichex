import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000'
})

// Send audio file → get risk result
export async function analyzeAudio(audioFile) {
  const formData = new FormData()
  formData.append('audio', audioFile)
  const response = await api.post('/analyze', formData)
  return response.data
}

// Get all call history from database
export async function getCallHistory() {
  const response = await api.get('/logs')
  return response.data
}

// Get recent 10 calls
export async function getRecentCalls() {
  const response = await api.get('/logs/recent')
  return response.data
}

// Get dashboard stats
export async function getStats() {
  const response = await api.get('/stats')
  return response.data
}

// Check server is running
export async function checkHealth() {
  const response = await api.get('/health')
  return response.data
}