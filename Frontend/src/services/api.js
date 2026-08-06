import axios from 'axios'

const api = axios.create({
    baseURL: 'http://127.0.0.1:5000'
})

// Send audio file → get risk result
export async function analyzeAudio(audioFile, onProgress) {
  const formData = new FormData()
  formData.append('audio', audioFile)
  const requestPath = '/analyze'
  const requestUrl = `${api.defaults.baseURL}${requestPath}`
  console.log('[analyzeAudio] Request URL:', requestUrl)

  try {
    const response = await api.post(requestPath, formData, {
      onUploadProgress: (evt) => {
        if (onProgress && evt.total) {
          onProgress(Math.round((evt.loaded * 100) / evt.total))
        }
      }
    })
    return response.data
  } catch (err) {
    console.error('[analyzeAudio] Axios error.code:', err.code)
    console.error('[analyzeAudio] Axios error.message:', err.message)
    console.error('[analyzeAudio] Axios response:', err.response)
    console.error('[analyzeAudio] Axios request URL:', err.config?.url)
    console.error('[analyzeAudio] Axios toJSON:', err.toJSON?.())
    throw err
  }
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
