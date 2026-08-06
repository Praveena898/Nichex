<template>
  <div class="page">
    <div class="content" style="padding-top:30px;">
      <div style="text-align:center;">
        <div class="risk-ring" style="width:150px;height:150px;border-radius:50%; margin:0 auto 16px; background:radial-gradient(circle,rgba(224,165,38,0.15),transparent 70%); box-shadow:0 0 0 8px rgba(224,165,38,0.18); display:flex;align-items:center;justify-content:center;">
          <div style="width:118px;height:118px;border-radius:50%;background:var(--card); display:flex;flex-direction:column;align-items:center;justify-content:center;">
            <div style="font-weight:800; font-size:15px;">{{ statusText }}</div>
            <div class="muted" style="font-size:10.5px; margin-top:2px;">{{ progress }}%</div>
          </div>
        </div>
        <p class="muted">{{ subText }}</p>
      </div>

      <div class="card" style="margin-top:20px;">
        <div class="row">
          <span>🎙️ Voice Pattern Analysis</span>
          <span class="pill" :class="voicePill">{{ voiceStatus }}</span>
        </div>
      </div>
      <div class="card">
        <div class="row">
          <span>🧠 Scam Language Detection</span>
          <span class="pill" :class="scamPill">{{ scamStatus }}</span>
        </div>
      </div>
      <div class="card">
        <div class="row"><span>📊 AI Detection Progress</span><span class="muted">{{ progress }}%</span></div>
        <div style="height:8px; background:var(--ring-off); border-radius:6px; margin-top:8px; overflow:hidden;">
          <div :style="{width:progress+'%', height:'100%', background:'var(--navy)', transition:'width .3s'}"></div>
        </div>
      </div>

      <!-- Error message if something goes wrong -->
      <div v-if="errorMsg" class="card" style="margin-top:10px; border: 1px solid red;">
        <p style="color:red; font-size:13px;">⚠️ {{ errorMsg }}</p>
        <button class="btn btn-ghost" style="margin-top:8px;" @click="$router.push('/dashboard')">Go Back</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { addCall } from '../callLog'
import { analyzeAudio } from '../services/api'

const route = useRoute()
const router = useRouter()

const progress  = ref(0)
const statusText = ref('RECORDING…')
const subText    = ref('Recording your call for analysis')
const voiceStatus = ref('Checking…')
const scamStatus  = ref('Checking…')
const voicePill   = ref('pill-amber')
const scamPill    = ref('pill-amber')
const errorMsg    = ref(null)

onMounted(async () => {
  try {
    // ── Step 1: Record 5 seconds from mic ────────────────────────────────────
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const mediaRecorder = new MediaRecorder(stream)
    const chunks = []

    mediaRecorder.ondataavailable = (e) => chunks.push(e.data)
    mediaRecorder.start()

    // Animate progress bar while recording
    const progressTimer = setInterval(() => {
      if (progress.value < 50) progress.value += 10
    }, 500)

    // Record for 5 seconds
    await new Promise(resolve => setTimeout(resolve, 5000))
    mediaRecorder.stop()
    stream.getTracks().forEach(t => t.stop())
    clearInterval(progressTimer)

    // ── Step 2: Send to Flask backend ─────────────────────────────────────────
    statusText.value = 'ANALYZING…'
    subText.value    = 'Running AI models on your call'
    progress.value   = 60

    const blob      = new Blob(chunks, { type: 'audio/webm' })
    const audioFile = new File([blob], 'call_recording.webm', { type: 'audio/webm' })

    const result = await analyzeAudio(audioFile)
    progress.value = 90

    // ── Step 3: Update UI with real results ───────────────────────────────────
    const deepfakePct = Math.round(result.deepfake_prob * 100)
    const scamPct     = Math.round(result.scam_language_prob * 100)

    voiceStatus.value = result.deepfake_prob > 0.5
      ? `${deepfakePct}% synthetic voice`
      : 'Real voice detected'
    scamStatus.value = result.scam_language_prob > 0.4
      ? `${scamPct}% scam language`
      : 'No scam language'

    voicePill.value = result.deepfake_prob > 0.5 ? 'pill-red' : 'pill-green'
    scamPill.value  = result.scam_language_prob > 0.4 ? 'pill-red' : 'pill-green'

    progress.value   = 100
    statusText.value = 'DONE'

    // ── Step 4: Save to callLog and route to result page ─────────────────────
    await new Promise(resolve => setTimeout(resolve, 500))

    // Map color from backend to tag used by router
    const tagMap = { GREEN: 'safe', YELLOW: 'suspicious', RED: 'scam' }
    const tag    = tagMap[result.color] || 'safe'

    const entry = addCall({
      name:       route.query.name  || 'Unknown Number',
      phone:      route.query.phone || '+91 98xxx xxxxx',
      tag,
      riskScore:  result.score,
      confidence: Math.round((1 - result.scam_language_prob) * 100),
      keywords:   result.transcript
        ? result.transcript.split(' ').filter(w =>
            ['otp','urgent','bank','transfer','money',"don't"].includes(w.toLowerCase())
          )
        : [],
      report:     result.transcript || 'Analysis complete.',
      duration:   '0m 5s'
    })

    router.push('/result/' + tag + '?callId=' + entry.id)

  } catch (err) {
    if (err.name === 'NotAllowedError') {
      errorMsg.value = 'Microphone permission denied. Please allow mic access and try again.'
    } else {
      errorMsg.value = `Analysis failed: ${err.message}. Make sure the backend server is reachable.`
    }
    progress.value   = 0
    statusText.value = 'ERROR'
    subText.value    = 'Something went wrong'
  }
})
</script>
