<template>
  <div class="page">
    <div class="topbar"><h2>{{ t('notifications.title') }}</h2><span style="width:36px;"></span></div>
    <div class="content">
      <div class="label">{{ t('notifications.scamAlerts') }}</div>
      <div class="card" v-for="c in scamCalls" :key="c.id" style="border-left:4px solid var(--red); margin-bottom:10px;">
        <div style="font-weight:700;">🔴 {{ t('notifications.scamDetected') }}</div>
        <div class="muted">{{ c.name }} · {{ c.time }}</div>
      </div>
      <div v-if="scamCalls.length === 0" class="card" style="margin-bottom:10px;">
        <p class="muted" style="margin:0;">{{ t('notifications.noScamAlerts') }}</p>
      </div>

      <div class="label">{{ t('notifications.familyNotifications') }}</div>
      <div class="card" v-for="a in familyAlerts" :key="a.id" style="border-left:4px solid var(--green); margin-bottom:10px;">
        <div style="font-weight:700; display:flex; align-items:center; gap:6px;"><Icon name="check" :size="15" color="var(--green)" /> {{ t('notifications.alertSentTo') }} {{ a.contactName }}</div>
        <div class="muted">{{ t('notifications.delivered') }} · {{ a.time }}</div>
      </div>
      <div v-if="familyAlerts.length === 0" class="card" style="margin-bottom:10px;">
        <p class="muted" style="margin:0;">{{ t('notifications.noFamilyAlerts') }}</p>
      </div>

      <div class="label">{{ t('notifications.securityUpdates') }}</div>
      <div class="card" style="border-left:4px solid var(--navy); margin-bottom:10px;">
        <div style="font-weight:700; display:flex; align-items:center; gap:6px;"><Icon name="lock" :size="15" color="var(--navy)" /> {{ t('notifications.modelUpdated') }}</div>
        <div class="muted">{{ t('notifications.newPatterns') }} · {{ t('notifications.yesterday') }}</div>
      </div>
    </div>
    <AppShell active="alerts" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppShell from '../components/AppShell.vue'
import { t } from '../i18n'
import Icon from '../components/Icon.vue'
import { loadCalls } from '../callLog'
import { loadFamilyAlerts } from '../familyAlertLog'

const scamCalls = ref([])
const familyAlerts = ref([])

onMounted(() => {
  scamCalls.value = loadCalls().filter(c => c.tag === 'scam').slice(0, 5)
  familyAlerts.value = loadFamilyAlerts().slice(0, 5)
})
</script>