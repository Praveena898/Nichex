<template>
  <div class="page">
    <div class="topbar"><h2>Notifications</h2><span style="width:36px;"></span></div>
    <div class="content">
      <div class="label">Scam Alerts</div>
      <div class="card" v-for="c in scamCalls" :key="c.id" style="border-left:4px solid var(--red); margin-bottom:10px;">
        <div style="font-weight:700;">🔴 Scam call detected</div>
        <div class="muted">{{ c.name }} · {{ c.time }}</div>
      </div>
      <div v-if="scamCalls.length === 0" class="card" style="margin-bottom:10px;">
        <p class="muted" style="margin:0;">No scam alerts yet.</p>
      </div>

      <div class="label">Family Notifications</div>
      <div class="card" v-for="a in familyAlerts" :key="a.id" style="border-left:4px solid var(--green); margin-bottom:10px;">
        <div style="font-weight:700;">✅ Alert sent to {{ a.contactName }}</div>
        <div class="muted">Delivered · {{ a.time }}</div>
      </div>
      <div v-if="familyAlerts.length === 0" class="card" style="margin-bottom:10px;">
        <p class="muted" style="margin:0;">No family alerts sent yet.</p>
      </div>

      <div class="label">Security Updates</div>
      <div class="card" style="border-left:4px solid var(--navy); margin-bottom:10px;">
        <div style="font-weight:700;">🔒 Detection model updated</div>
        <div class="muted">New scam-phrase patterns added · Yesterday</div>
      </div>
    </div>
    <AppShell active="alerts" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppShell from '../components/AppShell.vue'
import { loadCalls } from '../callLog'
import { loadFamilyAlerts } from '../familyAlertLog'

const scamCalls = ref([])
const familyAlerts = ref([])

onMounted(() => {
  scamCalls.value = loadCalls().filter(c => c.tag === 'scam').slice(0, 5)
  familyAlerts.value = loadFamilyAlerts().slice(0, 5)
})
</script>