<template>
  <div class="page">
    <div class="topbar" style="margin-bottom:8px;">
      <h2>{{ t('history.title') }}</h2>
      <span style="width:36px;"></span>
    </div>
    <div class="content" style="padding-top:14px;">
      <div class="row" style="gap:8px; margin-bottom:20px; align-items:center; flex-wrap:wrap;">
        <button v-for="f in filters" :key="f.key" class="pill" :class="active===f.key ? 'pill-green' : ''" :style="active!==f.key ? 'background:var(--card); color:var(--slate); border:1px solid var(--ring-off);' : ''" @click="active=f.key" style="flex:1; justify-content:center; min-width:70px;">{{ f.label }}</button>
        <button class="pill" style="background:var(--card); color:var(--navy); border:1px solid var(--ring-off); white-space:nowrap;" @click="showUploadModal = true">🎙️ Upload</button>
      </div>

      <router-link v-for="c in filtered" :key="c.id" :to="'/history/'+c.id" class="card" style="display:block; margin-bottom:10px;">
        <div class="row">
          <div>
            <div style="font-weight:700;">{{ c.name }}</div>
            <div class="muted">{{ c.time }}</div>
          </div>
          <span class="pill" :class="pillClass(c.tag)">{{ tagLabel(c.tag) }}</span>
        </div>
      </router-link>

      <div v-if="calls.length === 0" class="card" style="text-align:center;">
        <p class="muted" style="margin:0;">{{ t('history.noCallsYet') }}</p>
      </div>
    </div>
    <AppShell active="history" />

    <!-- Upload modal -->
    <div v-if="showUploadModal" style="position:fixed; inset:0; background:rgba(27,42,74,0.55); display:flex; align-items:center; justify-content:center; z-index:50; padding:20px;" @click.self="closeModal">
      <div style="background:var(--card); border-radius:20px; padding:26px 22px; width:100%; max-width:340px; box-shadow:0 20px 50px rgba(0,0,0,0.3);">

        <div class="row" style="margin-bottom:16px;">
          <h2 style="font-size:17px;">Upload Call Audio</h2>
          <button class="back-arrow" @click="closeModal" aria-label="Close">✕</button>
        </div>

        <!-- Idle -->
        <template v-if="uploadStatus === 'idle'">
          <p class="muted" style="margin-bottom:16px; font-size:13px;">Upload a recorded call (.mp3, .wav, .webm, .mpeg) to test detection.</p>

          <div
            class="dropzone"
            :class="{ 'dropzone-active': isDragging }"
            @click="fileInput.click()"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="onDrop"
          >
            <div style="font-size:30px; margin-bottom:6px;">🎙️</div>
            <div style="font-weight:700; font-size:13.5px; word-break:break-all;">
              {{ selectedFile ? selectedFile.name : (isDragging ? 'Drop the audio file here' : 'Tap or drag an audio file here') }}
            </div>
          </div>
          <input ref="fileInput" id="audioFile" type="file" accept="audio/*,video/mpeg,.mpeg,.mp3,.wav,.webm" style="display:none;" @change="onFileChange" />

          <div v-if="errorMsg" class="field-error" style="margin-top:10px;">{{ errorMsg }}</div>

          <button class="btn btn-primary" style="margin-top:16px;" :disabled="!selectedFile" @click="submitFile">Analyze This Call</button>
        </template>

        <!-- Analyzing -->
        <template v-else-if="uploadStatus === 'analyzing'">
          <div style="text-align:center; padding:16px 0;">
            <div style="width:56px;height:56px;border-radius:50%; background:rgba(224,165,38,0.15); border:2px solid var(--amber); display:flex;align-items:center;justify-content:center; margin:0 auto 14px;">
              <div style="width:22px;height:22px;border:3px solid rgba(224,165,38,0.3); border-top-color:var(--amber); border-radius:50%; animation:spin 0.8s linear infinite;"></div>
            </div>
            <div style="font-weight:700;">Analyzing Audio…</div>
            <p class="muted" style="margin-top:6px; font-size:13px;">Sending to the detection backend</p>
          </div>
        </template>

        <!-- Success -->
        <template v-else-if="uploadStatus === 'success'">
          <div style="text-align:center; padding:16px 0;">
            <div style="width:56px;height:56px;border-radius:50%; background:rgba(47,158,104,0.12); border:2px solid var(--green); display:flex;align-items:center;justify-content:center; font-size:24px; margin:0 auto 14px;">✅</div>
            <div style="font-weight:700;">Added to Call History</div>
            <p class="muted" style="margin:6px 0 16px; font-size:13px;">Result: <strong>{{ lastResultLabel }}</strong></p>
            <button class="btn btn-primary" @click="closeModal">Done</button>
          </div>
        </template>

        <!-- Error -->
        <template v-else-if="uploadStatus === 'error'">
          <div style="text-align:center; padding:16px 0;">
            <div style="width:56px;height:56px;border-radius:50%; background:rgba(214,69,69,0.12); border:2px solid var(--red); display:flex;align-items:center;justify-content:center; font-size:24px; margin:0 auto 14px;">⚠️</div>
            <div style="font-weight:700;">Couldn't Analyze Audio</div>
            <p class="muted" style="margin:6px 0 16px; font-size:13px;">{{ errorMsg }}</p>
            <button class="btn btn-ghost" @click="uploadStatus = 'idle'">Try Again</button>
          </div>
        </template>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppShell from '../components/AppShell.vue'
import { t } from '../i18n'
import { loadCalls, addCall } from '../callLog'
import { analyzeAudio } from '../services/api'

const active = ref('all')
const filters = computed(() => [
  { key: 'all', label: t('history.all') },
  { key: 'safe', label: t('history.safe') },
  { key: 'suspicious', label: t('history.suspicious') },
  { key: 'scam', label: t('history.scam') },
])

const calls = ref([])
const filtered = computed(() => active.value === 'all' ? calls.value : calls.value.filter(c => c.tag === active.value))

function pillClass(tag) {
  return { safe: 'pill-green', suspicious: 'pill-amber', scam: 'pill-red' }[tag]
}
function tagLabel(tag) {
  return t('history.' + tag)
}

function refreshCalls() {
  calls.value = loadCalls()
}

onMounted(refreshCalls)

const showUploadModal = ref(false)
const selectedFile = ref(null)
const uploadStatus = ref('idle') // idle | analyzing | success | error
const errorMsg = ref('')
const lastResultLabel = ref('')
const isDragging = ref(false)
const fileInput = ref(null)

function onFileChange(e) {
  errorMsg.value = ''
  const file = e.target.files[0]
  if (file) selectedFile.value = file
}

function isAudioLikeFile(file) {
  if (file.type.startsWith('audio/')) return true
  if (file.type === 'video/mpeg') return true // some browsers label .mpeg this way
  const ext = file.name.split('.').pop().toLowerCase()
  return ['mp3', 'wav', 'webm', 'mpeg', 'mpg', 'm4a', 'ogg'].includes(ext)
}

function onDrop(e) {
  isDragging.value = false
  errorMsg.value = ''
  const file = e.dataTransfer.files[0]
  if (!file) return
  if (!isAudioLikeFile(file)) {
    errorMsg.value = 'Please drop an audio file (.mp3, .wav, .webm, .mpeg).'
    return
  }
  selectedFile.value = file
}

function closeModal() {
  showUploadModal.value = false
  selectedFile.value = null
  uploadStatus.value = 'idle'
  errorMsg.value = ''
}

async function submitFile() {
  if (!selectedFile.value) return
  uploadStatus.value = 'analyzing'
  errorMsg.value = ''

  try {
    const userId = localStorage.getItem('digitalBodyguard.userId')
    const result = await analyzeAudio(selectedFile.value, Number(userId))

    const colorToTag = { GREEN: 'safe', YELLOW: 'suspicious', RED: 'scam' }
    const tag = colorToTag[result.color] || 'suspicious'

    addCall({
      name: selectedFile.value.name,
      phone: '—',
      tag,
      riskScore: result.score ?? 0,
      confidence: result.confidence ?? Math.round((result.score ?? 0)),
      keywords: result.keywords || [],
      report: result.transcript ? `Transcript: "${result.transcript}"` : 'No transcript available.',
      duration: '—'
    })

    lastResultLabel.value = tagLabel(tag)
    uploadStatus.value = 'success'
    refreshCalls()
  } catch (err) {
    uploadStatus.value = 'error'
    if (err.code === 'ERR_NETWORK') {
      errorMsg.value = "Couldn't reach the backend server. Make sure it's running on http://localhost:5000."
    } else {
      errorMsg.value = err.response?.data?.detail || 'Something went wrong analyzing this file.'
    }
  }
}
</script>

<style scoped>
.dropzone {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  border: 2px dashed var(--ring-off);
  border-radius: 14px;
  padding: 24px 14px;
  cursor: pointer;
  background: var(--paper);
  transition: border-color 0.15s ease, background 0.15s ease;
}
.dropzone:hover { border-color: var(--navy); }
.dropzone-active {
  border-color: var(--green);
  background: rgba(47,158,104,0.08);
}
@keyframes spin { to { transform: rotate(360deg); } }
.back-arrow {
  background: none;
  border: none;
  color: var(--navy);
  font-size: 16px;
  padding: 4px;
  cursor: pointer;
}
.field-error {
  color: var(--red);
  font-size: 12px;
}
</style>