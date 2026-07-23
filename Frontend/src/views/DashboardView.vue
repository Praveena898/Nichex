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
import { loadCalls, getStats } from '../callLog'

const userName = ref('there')
const recent = ref([])
const stats = ref({ total: 0, safe: 0, suspicious: 0, scam: 0 })

function pillClass(tag) {
  return { safe: 'pill-green', suspicious: 'pill-amber', scam: 'pill-red' }[tag]
}

onMounted(() => {
  const saved = localStorage.getItem('digitalBodyguard.account')
  if (saved) {
    const account = JSON.parse(saved)
    if (account.name) userName.value = account.name.split(' ')[0]
  }

  recent.value = loadCalls().slice(0, 3)
  stats.value = getStats()
})
</script>