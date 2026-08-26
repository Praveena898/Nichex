<template>
  <div class="page">
    <div class="topbar">
      <button
        class="back"
        :class="{ 'back-dark': darkMode }"
        @click="$router.back()"
        aria-label="Go back"
      >
        ←
      </button>

      <h2>{{ t('settings.title') }}</h2>

      <span class="topbar-spacer"></span>
    </div>

    <div class="content">
      <div class="card">
        <div class="row">
          <span class="setting-label">
            <Icon name="moon" :size="17" />
            {{ t('settings.darkMode') }}
          </span>

          <input
            type="checkbox"
            v-model="darkModeDraft"
          />
        </div>
      </div>

      <div class="card">
        <div class="row">
          <span class="setting-label">
            <Icon name="globe" :size="17" />
            {{ t('settings.language') }}
          </span>

          <select
            v-model="localeDraft"
            class="field language-select"
          >
            <option value="en">English</option>
            <option value="hi">हिन्दी (Hindi)</option>
            <option value="kok">कोंकणी (Konkani)</option>
            <option value="ml">മലയാളം (Malayalam)</option>
          </select>
        </div>
      </div>

      <div class="card">
        <div class="row">
          <span class="setting-label">
            <Icon name="accessibility" :size="17" />
            {{ t('settings.accessibility') }}
          </span>

          <input
            type="checkbox"
            v-model="largeTextDraft"
          />
        </div>
      </div>

      <div
        class="card expandable-card"
        @click="showNotifPanel = !showNotifPanel"
      >
        <div class="row">
          <span class="setting-label">
            <Icon name="bell" :size="17" />
            {{ t('settings.notifications') }}
          </span>

          <span
            class="arrow"
            :class="{ rotated: showNotifPanel }"
          >
            ›
          </span>
        </div>

        <div
          v-if="showNotifPanel"
          class="expand-panel"
          @click.stop
        >
          <div class="row panel-row">
            <span class="muted">
              Scam alerts
            </span>

            <input
              type="checkbox"
              v-model="notifDraft.scamAlerts"
            />
          </div>

          <div class="row panel-row">
            <span class="muted">
              Family notifications
            </span>

            <input
              type="checkbox"
              v-model="notifDraft.familyAlerts"
            />
          </div>

          <div class="row">
            <span class="muted">
              Security updates
            </span>

            <input
              type="checkbox"
              v-model="notifDraft.securityUpdates"
            />
          </div>
        </div>
      </div>

      <div
        class="card expandable-card"
        @click="showPrivacyPanel = !showPrivacyPanel"
      >
        <div class="row">
          <span class="setting-label">
            <Icon name="lock" :size="17" />
            {{ t('settings.privacy') }}
          </span>

          <span
            class="arrow"
            :class="{ rotated: showPrivacyPanel }"
          >
            ›
          </span>
        </div>

        <div
          v-if="showPrivacyPanel"
          class="expand-panel"
          @click.stop
        >
          <div class="row panel-row">
            <span class="muted">
              On-device call analysis
            </span>

            <input
              type="checkbox"
              v-model="privacyDraft.onDeviceOnly"
            />
          </div>

          <div class="row panel-row">
            <span class="muted">
              Store call transcripts
            </span>

            <input
              type="checkbox"
              v-model="privacyDraft.storeTranscripts"
            />
          </div>

          <div class="row">
            <span class="muted">
              Share data with family app
            </span>

            <input
              type="checkbox"
              v-model="privacyDraft.shareWithFamily"
            />
          </div>
        </div>
      </div>

      <button
        class="btn btn-primary"
        :disabled="!isDirty"
        @click="applySettings"
      >
        {{ isDirty ? t('common.applyChanges') : t('common.applied') }}
      </button>

      <div class="divider"></div>

      <button
        class="btn btn-ghost"
        @click="$router.push('/about')"
      >
        {{ t('settings.about') }}
      </button>

      <button
        class="btn btn-danger"
        @click="$router.push('/logout')"
      >
        {{ t('settings.logout') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  reactive,
  computed,
  onMounted
} from 'vue'

import {
  t,
  locale,
  setLocale
} from '../i18n'

import Icon from '../components/Icon.vue'

const darkMode = ref(false)
const darkModeDraft = ref(false)

const largeText = ref(false)
const largeTextDraft = ref(false)

const localeDraft = ref(locale.value)

const showNotifPanel = ref(false)
const showPrivacyPanel = ref(false)

const notifSettings = reactive({
  scamAlerts: true,
  familyAlerts: true,
  securityUpdates: false
})

const notifDraft = reactive({
  ...notifSettings
})

const privacySettings = reactive({
  onDeviceOnly: true,
  storeTranscripts: false,
  shareWithFamily: true
})

const privacyDraft = reactive({
  ...privacySettings
})

const isDirty = computed(() =>
  darkMode.value !== darkModeDraft.value ||
  largeText.value !== largeTextDraft.value ||
  locale.value !== localeDraft.value ||
  JSON.stringify(notifSettings) !==
    JSON.stringify(notifDraft) ||
  JSON.stringify(privacySettings) !==
    JSON.stringify(privacyDraft)
)

function applySettings() {
  darkMode.value = darkModeDraft.value
  largeText.value = largeTextDraft.value

  Object.assign(
    notifSettings,
    notifDraft
  )

  Object.assign(
    privacySettings,
    privacyDraft
  )

  document.documentElement.classList.toggle(
    'dark-mode',
    darkMode.value
  )

  document.documentElement.classList.toggle(
    'large-text',
    largeText.value
  )

  localStorage.setItem(
    'digitalBodyguard.darkMode',
    darkMode.value ? '1' : '0'
  )

  localStorage.setItem(
    'digitalBodyguard.largeText',
    largeText.value ? '1' : '0'
  )

  localStorage.setItem(
    'digitalBodyguard.notifSettings',
    JSON.stringify(notifSettings)
  )

  localStorage.setItem(
    'digitalBodyguard.privacySettings',
    JSON.stringify(privacySettings)
  )

  setLocale(localeDraft.value)
}

onMounted(() => {
  const savedDark =
    localStorage.getItem(
      'digitalBodyguard.darkMode'
    ) === '1'

  darkMode.value = savedDark
  darkModeDraft.value = savedDark

  const savedLarge =
    localStorage.getItem(
      'digitalBodyguard.largeText'
    ) === '1'

  largeText.value = savedLarge
  largeTextDraft.value = savedLarge

  document.documentElement.classList.toggle(
    'dark-mode',
    savedDark
  )

  document.documentElement.classList.toggle(
    'large-text',
    savedLarge
  )

  const savedNotif =
    localStorage.getItem(
      'digitalBodyguard.notifSettings'
    )

  if (savedNotif) {
    try {
      Object.assign(
        notifSettings,
        JSON.parse(savedNotif)
      )

      Object.assign(
        notifDraft,
        notifSettings
      )
    } catch (error) {
      console.error(
        'Could not load notification settings:',
        error
      )
    }
  }

  const savedPrivacy =
    localStorage.getItem(
      'digitalBodyguard.privacySettings'
    )

  if (savedPrivacy) {
    try {
      Object.assign(
        privacySettings,
        JSON.parse(savedPrivacy)
      )

      Object.assign(
        privacyDraft,
        privacySettings
      )
    } catch (error) {
      console.error(
        'Could not load privacy settings:',
        error
      )
    }
  }
})
</script>

<style scoped>
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.topbar h2 {
  margin: 0;
  text-align: center;
}

.topbar-spacer {
  width: 44px;
}

.back {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid #ddd;
  background: #ffffff;
  color: #0b2d5c;
  font-size: 28px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 0;
  font-family: Arial, sans-serif;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    border-color 0.2s ease,
    transform 0.2s ease;
}

.back:hover {
  background: #f2f2f2;
  color: #0b2d5c;
}

.back:active {
  transform: scale(0.94);
}

.back.back-dark {
  background: #1c2a46;
  border-color: #2b3d5f;
  color: #ffffff;
}

.back.back-dark:hover {
  background: #263654;
  color: #ffffff;
}

.setting-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.language-select {
  width: auto;
  margin: 0;
  padding: 6px 10px;
}

.expandable-card {
  cursor: pointer;
}

.arrow {
  display: inline-block;
  transition: transform 0.2s ease;
}

.arrow.rotated {
  transform: rotate(90deg);
}

.expand-panel {
  margin-top: 14px;
}

.panel-row {
  margin-bottom: 10px;
}

.muted {
  color: #777;
}

.divider {
  margin: 30px 0 18px;
}

.btn {
  width: 100%;
  cursor: pointer;
}

.btn:disabled {
  cursor: default;
  opacity: 1;
}
</style>