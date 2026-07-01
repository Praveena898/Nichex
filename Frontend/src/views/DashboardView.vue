<!-- DAY 3 -->
<template>
  <div class="page">
    <div class="topbar">
      <div>
        <div class="muted">Good afternoon,</div>
        <h2>Ramesh 👋</h2>
      </div>
      <router-link to="/settings" class="back">⚙️</router-link>
    </div>

    <div class="content">
      <div class="card" style="background:linear-gradient(135deg,var(--navy),#26395F); color:#fff;">
        <div class="row">
          <div>
            <div style="font-size:12px; opacity:0.8; letter-spacing:0.5px;">PROTECTION STATUS</div>
            <div style="font-size:18px; font-weight:800; margin-top:4px;">🟢 Active &amp; Monitoring</div>
          </div>
          <div style="font-size:30px;">🛡️</div>
        </div>
      </div>

      <div class="card">
        <div class="label" style="margin-bottom:10px;">Today's Activity</div>
        <div class="row">
          <div style="text-align:center;"><div style="font-size:20px;font-weight:800;">6</div><div class="muted">Calls</div></div>
          <div style="text-align:center;"><div style="font-size:20px;font-weight:800; color:var(--green);">5</div><div class="muted">Safe</div></div>
          <div style="text-align:center;"><div style="font-size:20px;font-weight:800; color:var(--amber);">0</div><div class="muted">Suspicious</div></div>
          <div style="text-align:center;"><div style="font-size:20px;font-weight:800; color:var(--red);">1</div><div class="muted">Scam</div></div>
        </div>
      </div>

      <div class="label">Recent Calls</div>
      <div class="card" v-for="c in recent" :key="c.name" style="margin-bottom:10px;">
        <div class="row">
          <div>
            <div style="font-weight:700;">{{ c.name }}</div>
            <div class="muted">{{ c.time }}</div>
          </div>
          <span class="pill" :class="c.pillClass">{{ c.tag }}</span>
        </div>
      </div>

      <div class="label">Quick Actions</div>
      <div class="row" style="gap:10px; margin-bottom:10px;">
        <button class="btn btn-ghost" style="flex:1;" @click="$router.push('/history')">📞 Call History</button>
        <button class="btn btn-ghost" style="flex:1;" @click="$router.push('/contacts')">👪 Contacts</button>
      </div>
      <button class="btn btn-danger" @click="$router.push('/family-alert')">🚨 Emergency — Alert My Family</button>
    </div>

    <AppShell active="home" />
  </div>
</template>

<script setup>
import AppShell from '../components/AppShell.vue'
const recent = [
  { name:'Riya (Daughter)', time:'Today, 9:10 AM', tag:'Safe', pillClass:'pill-green' },
  { name:'Unknown Number', time:'Today, 8:42 AM', tag:'Scam', pillClass:'pill-red' },
  { name:'Bank Helpline', time:'Yesterday, 6:15 PM', tag:'Safe', pillClass:'pill-green' },
]
</script>
