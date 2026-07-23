<template>
  <div class="page">
    <div class="topbar"><h2>{{ t('history.title') }}</h2><span style="width:36px;"></span></div>
    <div class="content">
      <div class="row" style="gap:8px; margin-bottom:14px;">
        <button v-for="f in filters" :key="f.key" class="pill" :class="active===f.key ? 'pill-green' : ''" :style="active!==f.key ? 'background:var(--card); color:var(--slate); border:1px solid var(--ring-off);' : ''" @click="active=f.key" style="flex:1; justify-content:center;">{{ f.label }}</button>
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
        <p class="muted" style="margin:0;">No calls yet. Once Digital Bodyguard analyzes a call, it'll show up here.</p>
      </div>
    </div>
    <AppShell active="history" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppShell from '../components/AppShell.vue'
import { t } from '../i18n'
import { loadCalls } from '../callLog'

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

onMounted(() => {
  calls.value = loadCalls()
})
</script>