Good catch — right now those toggles save instantly instead of waiting for "Apply Changes" like the rest. Let's fix that by giving them the same draft/applied pattern. Replace all of src/views/SettingsView.vue with:

vue
<!-- DAY 8 -->
<template>
  <div class="page">
    <div class="topbar">
      <router-link to="/dashboard" class="back">←</router-link>
      <h2>{{ t('settings.title') }}</h2>
      <span style="width:36px;"></span>
    </div>
    <div class="content">
      <div class="card">
        <div class="row">
          <span>🌙 {{ t('settings.darkMode') }}</span>
          <input type="checkbox" v-model="darkModeDraft" />
        </div>
      </div>
      <div class="card">
        <div class="row">
          <span>🌐 {{ t('settings.language') }}</span>
          <select v-model="localeDraft" class="field" style="width:auto; margin:0; padding:6px 10px;">
            <option value="en">English</option>
            <option value="hi">हिन्दी (Hindi)</option>
          </select>
        </div>
      </div>
      <div class="card">
        <div class="row">
          <span>♿ {{ t('settings.accessibility') }}</span>
          <input type="checkbox" v-model="largeTextDraft" />
        </div>
      </div>

      <!-- Notification Settings (expandable) -->
      <div class="card" style="cursor:pointer;" @click="showNotifPanel = !showNotifPanel">
        <div class="row">
          <span>🔔 {{ t('settings.notifications') }}</span>
          <span class="muted" :style="showNotifPanel ? 'transform:rotate(90deg); display:inline-block;' : ''">›</span>
        </div>
        <div v-if="showNotifPanel" style="margin-top:14px;" @click.stop>
          <div class="row" style="margin-bottom:10px;"><span class="muted">Scam alerts</span><input type="checkbox" v-model="notifDraft.scamAlerts" /></div>
          <div class="row" style="margin-bottom:10px;"><span class="muted">Family notifications</span><input type="checkbox" v-model="notifDraft.familyAlerts" /></div>
          <div class="row"><span class="muted">Security updates</span><input type="checkbox" v-model="notifDraft.securityUpdates" /></div>
        </div>
      </div>

      <!-- Privacy Settings (expandable) -->
      <div class="card" style="cursor:pointer;" @click="showPrivacyPanel = !showPrivacyPanel">
        <div class="row">
          <span>🔒 {{ t('settings.privacy') }}</span>
          <span class="muted" :style="showPrivacyPanel ? 'transform:rotate(90deg); display:inline-block;' : ''">›</span>
        </div>
        <div v-if="showPrivacyPanel" style="margin-top:14px;" @click.stop>
          <div class="row" style="margin-bottom:10px;"><span class="muted">On-device call analysis</span><input type="checkbox" v-model="privacyDraft.onDeviceOnly" /></div>
          <div class="row" style="margin-bottom:10px;"><span class="muted">Store call transcripts</span><input type="checkbox" v-model="privacyDraft.storeTranscripts" /></div>
          <div class="row"><span class="muted">Share data with family app</span><input type="checkbox" v-model="privacyDraft.shareWithFamily" /></div>
        </div>
      </div>

      <button class="btn btn-primary" :disabled="!isDirty" @click="applySettings">
        {{ isDirty ? t('common.applyChanges') : t('common.applied') }}
      </button>

      <div class="divider"></div>
      <button class="btn btn-ghost" @click="$router.push('/about')">{{ t('settings.about') }}</button>
      <button class="btn btn-danger" @click="$router.push('/logout')">{{ t('settings.logout') }}</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { t, locale, setLocale } from '../i18n'

const darkMode = ref(false)
const darkModeDraft = ref(false)

const largeText = ref(false)
const largeTextDraft = ref(false)

const localeDraft = ref(locale.value)

const showNotifPanel = ref(false)
const showPrivacyPanel = ref(false)

// "Applied" (currently active) state
const notifSettings = reactive({
  scamAlerts: true,
  familyAlerts: true,
  securityUpdates: false
})
const privacySettings = reactive({
  onDeviceOnly: true,
  storeTranscripts: false,
  shareWithFamily: true
})

// "Draft" (what the toggles currently show, not yet applied) state
const notifDraft = reactive({ ...notifSettings })
const privacyDraft = reactive({ ...privacySettings })

const isDirty = computed(() =>
  darkMode.value !== darkModeDraft.value ||
  largeText.value !== largeTextDraft.value ||
  locale.value !== localeDraft.value ||
  JSON.stringify(notifSettings) !== JSON.stringify(notifDraft) ||
  JSON.stringify(privacySettings) !== JSON.stringify(privacyDraft)
)

function applySettings() {
  darkMode.value = darkModeDraft.value
  largeText.value = largeTextDraft.value
  Object.assign(notifSettings, notifDraft)
  Object.assign(privacySettings, privacyDraft)

  document.documentElement.classList.toggle('dark-mode', darkMode.value)
  document.documentElement.classList.toggle('large-text', largeText.value)

  localStorage.setItem('digitalBodyguard.darkMode', darkMode.value ? '1' : '0')
  localStorage.setItem('digitalBodyguard.largeText', largeText.value ? '1' : '0')
  localStorage.setItem('digitalBodyguard.notifSettings', JSON.stringify(notifSettings))
  localStorage.setItem('digitalBodyguard.privacySettings', JSON.stringify(privacySettings))

  setLocale(localeDraft.value)
}

onMounted(() => {
  const savedDark = localStorage.getItem('digitalBodyguard.darkMode') === '1'
  const savedLarge = localStorage.getItem('digitalBodyguard.largeText') === '1'

  darkMode.value = savedDark
  darkModeDraft.value = savedDark
  largeText.value = savedLarge
  largeTextDraft.value = savedLarge

  document.documentElement.classList.toggle('dark-mode', savedDark)
  document.documentElement.classList.toggle('large-text', savedLarge)

  const savedNotif = localStorage.getItem('digitalBodyguard.notifSettings')
  if (savedNotif) {
    Object.assign(notifSettings, JSON.parse(savedNotif))
    Object.assign(notifDraft, notifSettings)
  }

  const savedPrivacy = localStorage.getItem('digitalBodyguard.privacySettings')
  if (savedPrivacy) {
    Object.assign(privacySettings, JSON.parse(savedPrivacy))
    Object.assign(privacyDraft, privacySettings)
  }
})
</script>