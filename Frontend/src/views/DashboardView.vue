<template>
  <div class="page">
    <div class="topbar">
      <div>
        <div class="muted">{{ t('dashboard.greeting') }}</div>
        <h2>{{ userName }} 👋</h2>
      </div>
      <router-link to="/settings" class="back">⚙️</router-link>
    </div>

    <div class="content">
      <div class="card" style="background:linear-gradient(135deg,#1B2A4A,#26395F); color:#fff;">
        <div class="row">
          <div>
            <div style="font-size:12px; opacity:0.8; letter-spacing:0.5px;">{{ t('dashboard.status') }}</div>
            <div style="font-size:18px; font-weight:800; margin-top:4px;">🟢 {{ t('dashboard.active') }}</div>
          </div>
          <div style="font-size:30px;">🛡️</div>
        </div>
      </div>

      <div v-if="loading" class="card">
        <p class="muted" style="margin:0;">Loading...</p>
      </div>
      <div v-else-if="error" class="card">
        <p class="muted" style="margin:0;">Couldn't load your data. Pull to refresh or try again later.</p>
      </div>

      <template v-else>
        <div class="card">
          <div class="label" style="margin-bottom:10px;">{{ t('dashboard.today') }}</div>
          <div class="row">
            <div style="text-align:center;"><div style="font-size:20px;font-weight:800;">{{ stats.total }}</div><div class="muted">{{ t('dashboard.calls') }}</div></div>
            <div style="text-align:center;"><div style="font-size:20px;font-weight:800; color:var(--green);">{{ stats.safe }}</div><div class="muted">{{ t('dashboard.safe') }}</div></div>
            <div style="text-align:center;"><div style="font-size:20px;font-weight:800; color:var(--amber);">{{ stats.suspicious }}</div><div class="muted">{{ t('dashboard.suspicious') }}</div></div>
            <div style="text-align:center;"><div style="font-size:20px;font-weight:800; color:var(--red);">{{ stats.scam }}</div><div class="muted">{{ t('dashboard.scam') }}</div></div>
          </div>
        </div>

        <div class="label">{{ t('dashboard.recent') }}</div>
        <div class="card" v-for="c in recent" :key="c.id" style="margin-bottom:10px;">
          <div class="row">
            <div>
              <div style="font-weight:700;">{{ c.name }}</div>
              <div class="muted">{{ c.time }}</div>
            </div>
            <span class="pill" :class="pillClass(c.tag)">{{ t('dashboard.' + c.tag) }}</span>
          </div>
        </div>
        <div v-if="recent.length === 0" class="card">
          <p class="muted" style="margin:0;">No calls analyzed yet.</p>
        </div>
      </template>

      <div class="label">{{ t('dashboard.quickActions') }}</div>
      <div class="row" style="gap:10px; margin-bottom:10px;">
        <button class="btn btn-ghost" style="flex:1;" @click="$router.push('/history')">📞 {{ t('dashboard.callHistory') }}</button>
        <button class="btn btn-ghost" style="flex:1;" @click="$router.push('/contacts')">👪 {{ t('dashboard.contacts') }}</button>
      </div>
      <button class="btn btn-danger" @click="$router.push('/family-alert')">🚨 {{ t('dashboard.emergency') }}</button>
    </div>

    <AppShell active="home" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppShell from '../components/AppShell.vue'
import { t } from '../i18n'
import { getStats, getRecentCalls } from '../services/api.js'

const userName = ref('there')
const recent = ref([])
const stats = ref({ total: 0, safe: 0, suspicious: 0, scam: 0 })
const loading = ref(true)
const error = ref(null)

function pillClass(tag) {
  return { safe: 'pill-green', suspicious: 'pill-amber', scam: 'pill-red' }[tag]
}

// Backend sends color as "RED" / "YELLOW" / "GREEN" (see crud.py get_stats / CallLog.color).
// Maps that into the safe/suspicious/scam tag used by the template and pillClass().
function scoreToTag(call) {
  const map = { GREEN: 'safe', YELLOW: 'suspicious', RED: 'scam' }
  if (call.color && map[call.color.toUpperCase()]) {
    return map[call.color.toUpperCase()]
  }
  // Fallback if color is ever missing — risk_score is 0-100 per the pipeline
  if (call.score >= 70) return 'scam'
  if (call.score >= 30) return 'suspicious'
  return 'safe'
}

onMounted(async () => {
  const saved = localStorage.getItem('digitalBodyguard.account')
  if (saved) {
    const account = JSON.parse(saved)
    if (account.name) userName.value = account.name.split(' ')[0]
  }

  try {
    const [apiStats, apiCalls] = await Promise.all([getStats(), getRecentCalls()])

    // Matches schemas.StatsResponse exactly:
    // total_chunks_analyzed, red_alerts, yellow_warnings, safe_chunks,
    // family_alerts_sent, average_risk_score
    stats.value = {
      total: apiStats.total_chunks_analyzed,
      safe: apiStats.safe_chunks,
      suspicious: apiStats.yellow_warnings,
      scam: apiStats.red_alerts
    }

    // Matches schemas.CallLogResponse: log_id, user_id, timestamp, risk_score,
    // color, deepfake_prob, scam_prob, transcript, alert_sent, chunk_num
    recent.value = apiCalls.slice(0, 3).map((c, i) => ({
      id: c.log_id ?? i,
      // No caller-name field in CallLogResponse — using transcript as a stand-in.
      // Swap this if you add a caller_number/name field later.
      name: c.transcript ? c.transcript.slice(0, 40) : 'Unknown caller',
      time: c.timestamp,
      tag: scoreToTag({ color: c.color, score: c.risk_score })
    }))
  } catch (e) {
    error.value = e
    console.error('Failed to load dashboard data', e)
  } finally {
    loading.value = false
  }
})
</script>