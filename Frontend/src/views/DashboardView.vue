<template>
  <div class="page">
    <div class="topbar">
      <div>
        <div class="muted">{{ t('dashboard.greeting') }}</div>
        <h2>{{ userName }}</h2>
      </div>

      <div class="dashboard-actions">
        <router-link
          to="/settings"
          class="settings-button"
          aria-label="Settings"
          title="Settings"
        >
          <Icon name="settings" :size="19" />
        </router-link>
      </div>

      <input
        ref="fileInput"
        type="file"
        accept="audio/*"
        style="display:none"
        @change="handleUpload"
      />
    </div>

    <div class="content">
      <div
        class="card"
        style="background:linear-gradient(135deg,#1B2A4A,#26395F); color:#fff;"
      >
        <div class="row">
          <div>
            <div
              style="font-size:12px; opacity:0.8; letter-spacing:0.5px;"
            >
              {{ t('dashboard.status') }}
            </div>

            <div
              style="font-size:18px; font-weight:800; margin-top:4px; display:flex; align-items:center; gap:6px;"
            >
              <Icon
                name="check-circle"
                :size="18"
                color="#4ADE80"
              />

              {{ t('dashboard.active') }}
            </div>
          </div>

          <Icon name="shield" :size="30" />
        </div>
      </div>

      <div class="card">
        <div
          class="label"
          style="margin-bottom:10px;"
        >
          {{ t('dashboard.today') }}
        </div>

        <div class="row">
          <div class="stat">
            <div class="stat-number">
              {{ stats.total }}
            </div>
            <div class="muted">
              {{ t('dashboard.calls') }}
            </div>
          </div>

          <div class="stat">
            <div
              class="stat-number"
              style="color:var(--green);"
            >
              {{ stats.safe }}
            </div>
            <div class="muted">
              {{ t('dashboard.safe') }}
            </div>
          </div>

          <div class="stat">
            <div
              class="stat-number"
              style="color:var(--amber);"
            >
              {{ stats.suspicious }}
            </div>
            <div class="muted">
              {{ t('dashboard.suspicious') }}
            </div>
          </div>

          <div class="stat">
            <div
              class="stat-number"
              style="color:var(--red);"
            >
              {{ stats.scam }}
            </div>
            <div class="muted">
              {{ t('dashboard.scam') }}
            </div>
          </div>
        </div>
      </div>

      <div class="label">
        {{ t('dashboard.recent') }}
      </div>

      <div
        class="card recent-card"
        v-for="c in recent"
        :key="c.id"
      >
        <div class="row">
          <div>
            <div class="caller-name">
              {{ c.name }}
            </div>

            <div class="muted">
              {{ c.time }}
            </div>
          </div>

          <span
            class="pill"
            :class="pillClass(c.tag)"
          >
            {{ t('dashboard.' + c.tag) }}
          </span>
        </div>
      </div>

      <div
        v-if="recent.length === 0"
        class="card"
      >
        <p
          class="muted"
          style="margin:0;"
        >
          No calls analyzed yet.
        </p>
      </div>

      <div class="label">
        {{ t('dashboard.quickActions') }}
      </div>

      <div
        class="row"
        style="gap:10px; margin-bottom:10px;"
      >
        <button
          class="btn btn-ghost"
          style="flex:1; display:flex; align-items:center; justify-content:center; gap:8px;"
          @click="$router.push('/history')"
        >
          <Icon name="phone" :size="16" />
          {{ t('dashboard.callHistory') }}
        </button>

        <button
          class="btn btn-ghost"
          style="flex:1; display:flex; align-items:center; justify-content:center; gap:8px;"
          @click="$router.push('/contacts')"
        >
          <Icon name="users" :size="16" />
          {{ t('dashboard.contacts') }}
        </button>
      </div>

      <button
        class="btn btn-danger"
        style="display:flex; align-items:center; justify-content:center; gap:8px;"
        @click="$router.push('/family-alert')"
      >
        <Icon
          name="alert-triangle"
          :size="16"
        />
        {{ t('dashboard.emergency') }}
      </button>
    </div>

    <AppShell
      active="home"
      :uploading="uploading"
      @upload="triggerUpload"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppShell from '../components/AppShell.vue'
import Icon from '../components/Icon.vue'
import { t } from '../i18n'
import {
  getStats,
  getRecentCalls,
  analyzeAudio
} from '../services/api.js'

const router = useRouter()

const userName = ref('there')
const recent = ref([])

const stats = ref({
  total: 0,
  safe: 0,
  suspicious: 0,
  scam: 0
})

const fileInput = ref(null)
const uploading = ref(false)

function pillClass(tag) {
  return {
    safe: 'pill-green',
    suspicious: 'pill-amber',
    scam: 'pill-red'
  }[tag]
}

function triggerUpload() {
  if (!uploading.value) {
    fileInput.value?.click()
  }
}

async function handleUpload(event) {
  const file = event.target.files[0]

  event.target.value = ''

  if (!file) {
    return
  }

  uploading.value = true

  try {
    const result = await analyzeAudio(file)

    let callId = ''

    try {
      const recentCalls = await getRecentCalls()

      if (
        recentCalls &&
        recentCalls.length
      ) {
        callId = recentCalls[0].log_id
      }
    } catch (e) {
      console.error(
        'Could not fetch new log id:',
        e
      )
    }

    const routeMap = {
      RED: '/result/scam',
      YELLOW: '/result/suspicious',
      GREEN: '/result/safe'
    }

    const base =
      routeMap[result.color] ||
      '/result/safe'

    router.push(
      callId
        ? base + '?callId=' + callId
        : base
    )
  } catch (err) {
    console.error(
      'Audio upload/analysis failed:',
      err
    )
  } finally {
    uploading.value = false
  }
}

onMounted(async () => {
  const saved =
    localStorage.getItem(
      'digitalBodyguard.account'
    )

  if (saved) {
    try {
      const account = JSON.parse(saved)

      if (account.name) {
        userName.value =
          account.name.split(' ')[0]
      }
    } catch (error) {
      console.error(
        'Could not load account:',
        error
      )
    }
  }

  try {
    const backendStats =
      await getStats()

    const total =
      backendStats.total_chunks_analyzed ?? 0

    const scam =
      backendStats.red_alerts ?? 0

    const safe =
      backendStats.safe_chunks ?? 0

    const suspicious =
      Math.max(
        total - safe - scam,
        0
      )

    stats.value = {
      total,
      safe,
      suspicious,
      scam
    }

    const recentCalls =
      await getRecentCalls()

    recent.value =
      recentCalls
        .slice(0, 3)
        .map(log => ({
          id: log.log_id,
          name: 'Unknown Number',
          time: new Date(
            log.timestamp
          ).toLocaleString(
            [],
            {
              hour: '2-digit',
              minute: '2-digit'
            }
          ),
          tag:
            log.color === 'RED'
              ? 'scam'
              : log.color === 'YELLOW'
                ? 'suspicious'
                : 'safe'
        }))
  } catch (err) {
    console.error(
      'Failed to load dashboard data from backend:',
      err
    )
  }
})
</script>

<style scoped>
.dashboard-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.settings-button {
  width: 36px !important;
  height: 36px !important;
  min-width: 36px !important;
  min-height: 36px !important;
  padding: 0 !important;
  margin: 0 !important;

  border-radius: 50% !important;

  display: flex !important;
  align-items: center !important;
  justify-content: center !important;

  text-decoration: none !important;

  transition:
    background 0.2s ease,
    color 0.2s ease,
    border-color 0.2s ease;
}

:global(html:not(.dark-mode)) .settings-button {
  background: #d4d4d4 !important;
  border: 1px solid #aaaaaa !important;
  color: #111827 !important;
}

:global(html:not(.dark-mode)) .settings-button:hover {
  background: #bcbcbc !important;
  border-color: #999999 !important;
  color: #000000 !important;
}

:global(html.dark-mode) .settings-button {
  background: #ffffff !important;
  border: 1px solid #ffffff !important;
  color: #111827 !important;
}

:global(html.dark-mode) .settings-button:hover {
  background: #e5e7eb !important;
  border-color: #e5e7eb !important;
  color: #000000 !important;
}

.settings-button :deep(svg) {
  color: currentColor !important;
  stroke: currentColor !important;
}

.icon-svg {
  width: 18px;
  height: 18px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.icon-svg.spin {
  animation: icon-spin 0.9s linear infinite;
}

.stat {
  text-align: center;
}

.stat-number {
  font-size: 20px;
  font-weight: 800;
}

.recent-card {
  margin-bottom: 10px;
}

.caller-name {
  font-weight: 700;
}

@keyframes icon-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>