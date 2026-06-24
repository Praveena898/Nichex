
<template>
  <div class="shell">
    <div class="topbar">
      <div class="logo">🛡 Digital Bodyguard</div>
      <div class="status-pill">Protected</div>
    </div>

    <aside class="sidebar">
      <div class="nav-item active">Dashboard</div>
      <div class="nav-item">Call Analysis</div>
      <div class="nav-item">Messages</div>
      <div class="nav-item">Deepfake Scan</div>
    </aside>

    <main class="main">
      <h1>Threat Dashboard</h1>

      <div class="stat-grid">
        <div class="stat-card" v-for="card in stats" :key="card.label">
          <div class="stat-label">{{ card.label }}</div>
          <div class="stat-value">{{ card.value }}</div>
          <div class="stat-sub">{{ card.sub }}</div>
        </div>
      </div>

      <div class="panel">
        <h3>Recent Threat Events</h3>
        <div v-for="threat in threats" :key="threat.id" class="threat-item">
          <strong>{{ threat.name }}</strong>
          <p>{{ threat.desc }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const stats = ref([
  { label: 'Threats Blocked', value: '12', sub: 'Today' },
  { label: 'Suspicious', value: '4', sub: 'Awaiting review' },
  { label: 'Calls Analyzed', value: '38', sub: 'Last 24 hours' },
  { label: 'AI Accuracy', value: '98.4%', sub: 'Model confidence' }
])

const threats = ref([
  { id: 1, name: 'OTP Fraud Attempt', desc: 'Fake bank SMS requesting OTP code' },
  { id: 2, name: 'Suspicious Call', desc: 'Caller claiming to be from TRAI' },
  { id: 3, name: 'Deepfake Voice Alert', desc: 'AI-cloned voice detected' }
])
</script>

<style scoped>
body{margin:0}
.shell{display:grid;grid-template-columns:220px 1fr;background:#0B1120;color:white;min-height:100vh}
.topbar{grid-column:1/-1;padding:15px;background:#141E35;display:flex;justify-content:space-between}
.sidebar{background:#141E35;padding:20px}
.nav-item{padding:10px}
.main{padding:20px}
.stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.stat-card,.panel{background:#141E35;padding:15px;border-radius:12px}
.threat-item{padding:10px 0;border-bottom:1px solid #333}
</style>
