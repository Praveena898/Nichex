<template>
  <div class="page">
     <button class="back-button" @click="$router.push('/dashboard')">
      ←
    </button>
    <div class="content" style="padding-top: 24px;">

      <!-- Header -->
      <div style="text-align:center; margin-bottom: 24px;">
        <h2 style="font-weight:800;">🛡️ Live Call Monitor</h2>
        <p class="muted">{{ isMonitoring ? 'Monitoring active...' : 'Tap Start to begin monitoring' }}</p>
      </div>

      <!-- Color Ring -->
      <div style="display:flex; justify-content:center; margin-bottom:24px;">
        <div :class="['color-ring', ringClass]">
          <div class="ring-inner">
            <span style="font-size:36px;">{{ colorIcon }}</span>
            <span style="font-weight:800; font-size:14px; margin-top:4px;">{{ colorLabel }}</span>
            <span class="muted" style="font-size:12px;">{{ score }}/100</span>
          </div>
        </div>
      </div>

      <!-- Alert Banner -->
      <div v-if="color === 'RED'" class="alert-banner red">
        🚨 HIGH RISK — Possible scam detected!
        Hang up immediately.
      </div>
      <div v-else-if="color === 'YELLOW'" class="alert-banner yellow">
        ⚠️ Suspicious call. Do NOT share OTP or personal details.
      </div>
      <div v-else-if="isMonitoring" class="alert-banner green">
        ✅ Call appears safe. Monitoring continues...
      </div>

      <!-- Stats Cards -->
      <div class="card" v-if="isMonitoring || transcript">
        <div class="row">
          <span>🎙️ Voice (Deepfake)</span>
          <span class="muted">{{ (deepfakeProb * 100).toFixed(0) }}% synthetic</span>
        </div>
        <div class="progress-bar">
          <div :style="{ width: (deepfakeProb * 100) + '%', background: '#8b5cf6' }"></div>
        </div>
      </div>

      <div class="card" v-if="isMonitoring || transcript">
        <div class="row">
          <span>🧠 Scam Language</span>
          <span class="muted">{{ (scamProb * 100).toFixed(0) }}% scam</span>
        </div>
        <div class="progress-bar">
          <div :style="{ width: (scamProb * 100) + '%', background: '#ef4444' }"></div>
        </div>
      </div>

      <!-- Transcript -->
      <div class="card" v-if="transcript">
        <div class="label">📝 Last heard:</div>
        <div class="muted" style="font-size:13px; margin-top:6px; font-style:italic;">
          "{{ transcript }}"
        </div>
      </div>

      <!-- Chunk counter -->
      <div v-if="isMonitoring" style="text-align:center; margin: 8px 0;">
        <span class="muted" style="font-size:12px;">
          Chunk #{{ chunkCount }} — analyzing every 3 seconds
        </span>
      </div>

      <!-- Error -->
      <div v-if="errorMsg" class="card" style="border: 1px solid red; margin-top:8px;">
        <p style="color:red; font-size:13px;">⚠️ {{ errorMsg }}</p>
      </div>

      <!-- Start / Stop Button -->
      <div style="margin-top: 24px;">
        <button
          v-if="!isMonitoring"
          class="btn btn-primary"
          style="width:100%; background:#22c55e; color:#000;"
          @click="startMonitoring"
          :disabled="connecting"
        >
          {{ connecting ? 'Starting...' : '📞 Start Monitoring' }}
        </button>
        <button
          v-else
          class="btn btn-danger"
          style="width:100%;"
          @click="stopMonitoring"
        >
          🛑 Stop Monitoring
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { VoiceRecorder } from 'capacitor-voice-recorder'

// ── Config ──────────────────────────────────────────────────────────────────
const BACKEND_URL = 'http://127.0.0.1:5000'
const CHUNK_DURATION = 3000

// ── State ────────────────────────────────────────────────────────────────────
const isMonitoring = ref(false)
const connecting = ref(false)
const color = ref('')
const score = ref(0)
const deepfakeProb = ref(0)
const scamProb = ref(0)
const transcript = ref('')
const chunkCount = ref(0)
const errorMsg = ref(null)

// Used to stop the continuous recording loop
let shouldContinue = false

// ── Computed ─────────────────────────────────────────────────────────────────
const ringClass = computed(() => {
  if (color.value === 'RED') return 'ring-red'
  if (color.value === 'YELLOW') return 'ring-yellow'
  if (color.value === 'GREEN') return 'ring-green'
  return 'ring-idle'
})

const colorIcon = computed(() => {
  if (color.value === 'RED') return '🔴'
  if (color.value === 'YELLOW') return '🟡'
  if (color.value === 'GREEN') return '🟢'
  return '⚪'
})

const colorLabel = computed(() => {
  if (color.value === 'RED') return 'HIGH RISK'
  if (color.value === 'YELLOW') return 'SUSPICIOUS'
  if (color.value === 'GREEN') return 'SAFE'
  return 'IDLE'
})

// ── Helper: wait ─────────────────────────────────────────────────────────────
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

// ── Start Monitoring ─────────────────────────────────────────────────────────
async function startMonitoring() {
  errorMsg.value = null
  connecting.value = true

  try {
    // Check microphone capability
    const canRecord = await VoiceRecorder.canDeviceVoiceRecord()

    if (!canRecord.value) {
      throw new Error('This device cannot record audio.')
    }

    // Request/check microphone permission
    const permission =
      await VoiceRecorder.requestAudioRecordingPermission()

    if (!permission.value) {
      throw new Error('Microphone permission denied.')
    }

    // Start monitoring
    shouldContinue = true
    isMonitoring.value = true
    connecting.value = false
    chunkCount.value = 0
    color.value = 'GREEN'

    console.log('NATIVE MIC: Monitoring started')

    // Start continuous 3-second chunk processing
    recordChunkLoop()

  } catch (err) {
    console.error('NATIVE MIC ERROR:', err)

    connecting.value = false
    isMonitoring.value = false
    shouldContinue = false

    errorMsg.value =
      'Could not start microphone: ' +
      (err.message || err)
  }
}

// ── Continuous 3-second recording loop ───────────────────────────────────────
async function recordChunkLoop() {
  while (shouldContinue) {

    try {
      console.log('Starting 3-second recording...')

      // Start native Android recording
      await VoiceRecorder.startRecording()

      console.log('Recording started')

      // Record for exactly 3 seconds
      await sleep(CHUNK_DURATION)

      // If user pressed Stop during those 3 seconds
      if (!shouldContinue) {
        try {
          await VoiceRecorder.stopRecording()
        } catch (e) {
          console.log('Recording already stopped')
        }

        break
      }

      // Stop the native recording
      const recording = await VoiceRecorder.stopRecording()

      console.log(
        'Recording stopped:',
        recording.value.msDuration,
        'ms'
      )

      const base64Audio = recording.value.recordDataBase64
      const mimeType =
        recording.value.mimeType || 'audio/aac'

      if (!base64Audio) {
        console.warn('No audio data received')
        continue
      }

      // Convert Base64 → Blob
      const audioBlob = base64ToBlob(
        base64Audio,
        mimeType
      )

      console.log(
        'Audio chunk size:',
        audioBlob.size,
        'bytes'
      )

      // Send this 3-second chunk to backend
      await sendChunkToBackend(
        audioBlob,
        mimeType
      )

    } catch (err) {

      console.error('CHUNK ERROR:', err)

      if (shouldContinue) {
        errorMsg.value =
          `Recording/analysis failed: ${err.message || err}`

        // Don't completely kill monitoring because of one bad chunk
        await sleep(500)
      }
    }
  }

  console.log('Recording loop stopped')
}

// ── Convert Base64 audio to Blob ─────────────────────────────────────────────
function base64ToBlob(base64, mimeType) {

  const byteCharacters = atob(base64)
  const byteArrays = []

  const sliceSize = 1024

  for (
    let offset = 0;
    offset < byteCharacters.length;
    offset += sliceSize
  ) {

    const slice = byteCharacters.slice(
      offset,
      offset + sliceSize
    )

    const byteNumbers = new Array(slice.length)

    for (let i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i)
    }

    const byteArray = new Uint8Array(byteNumbers)

    byteArrays.push(byteArray)
  }

  return new Blob(byteArrays, {
    type: mimeType
  })
}

// ── Send chunk to FastAPI ─────────────────────────────────────────────────────
async function sendChunkToBackend(audioBlob, mimeType) {

  try {

    const extension =
      mimeType.includes('aac')
        ? 'aac'
        : mimeType.includes('mp4')
          ? 'mp4'
          : 'audio'

    const file = new File(
      [audioBlob],
      `chunk_${chunkCount.value}.${extension}`,
      {
        type: mimeType
      }
    )

    const formData = new FormData()

    formData.append(
      'audio',
      file
    )

    console.log(
      `Sending chunk #${chunkCount.value} to backend...`
    )

    const response = await fetch(
      `${BACKEND_URL}/live-analyze`,
      {
        method: 'POST',
        body: formData
      }
    )

    if (!response.ok) {
      throw new Error(
        `Server error ${response.status}`
      )
    }

    const result = await response.json()

    // Update UI
    chunkCount.value += 1

    color.value =
      result.color || 'GREEN'

    score.value =
      result.score || 0

    deepfakeProb.value =
      result.deepfake_prob || 0

    scamProb.value =
      result.scam_language_prob || 0

    transcript.value =
      result.transcript || ''

    errorMsg.value = null

    console.log(
      `Chunk #${chunkCount.value} analyzed successfully`
    )

  } catch (err) {

    console.error(
      'BACKEND ERROR:',
      err
    )

    errorMsg.value =
      `Analysis failed: ${err.message}. Is backend running?`
  }
}

// ── Stop Monitoring ───────────────────────────────────────────────────────────
async function stopMonitoring() {

  console.log('Stopping monitoring...')

  // Tell loop to stop
  shouldContinue = false

  // Try to stop native recorder if currently recording
  try {

    const status =
      await VoiceRecorder.getCurrentStatus()

    if (
      status.status === 'RECORDING'
    ) {

      await VoiceRecorder.stopRecording()

      console.log(
        'Current recording stopped'
      )
    }

  } catch (err) {

    console.log(
      'No active recording to stop'
    )
  }

  // Reset UI
  isMonitoring.value = false
  connecting.value = false

  color.value = ''
  score.value = 0

  deepfakeProb.value = 0
  scamProb.value = 0

  transcript.value = ''
  chunkCount.value = 0
}
</script>
<style scoped>

.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
  border: none;
  background: transparent;
  font-size: 32px;
  color: #1B2A4A;
  cursor: pointer;
  z-index: 10;
}
.color-ring {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  border: 8px solid #333;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.5s ease;
}

.ring-green  { border-color: #22c55e; box-shadow: 0 0 30px #22c55e88; }
.ring-yellow { border-color: #eab308; box-shadow: 0 0 30px #eab30888; }
.ring-red    { border-color: #ef4444; box-shadow: 0 0 40px #ef444499; animation: pulse 1s infinite; }
.ring-idle   { border-color: #444; }

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 20px #ef444488; }
  50%       { box-shadow: 0 0 50px #ef4444cc; }
}

.ring-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 140px;
  height: 140px;
  border-radius: 50%;
  background: var(--card, #1a1a2e);
}

.alert-banner {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 13px;
  font-weight: 500;
}
.red    { background: #450a0a; border: 1px solid #ef4444; color: #fca5a5; }
.yellow { background: #422006; border: 1px solid #eab308; color: #fde047; }
.green  { background: #052e16; border: 1px solid #22c55e; color: #86efac; }

.progress-bar {
  height: 6px;
  background: #333;
  border-radius: 3px;
  margin-top: 8px;
  overflow: hidden;
}
.progress-bar div {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}
</style>
