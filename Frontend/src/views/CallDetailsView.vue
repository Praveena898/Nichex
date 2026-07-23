<template>
  <div class="page">
    <div class="topbar">
      <button class="back-arrow" @click="$router.back()" aria-label="Go back">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M15 18l-6-6 6-6" />
        </svg>
      </button>
      <h2>Call Details</h2>
      <span style="width:36px;"></span>
    </div>

    <div class="content" v-if="call">
      <div class="card">
        <div class="label" style="margin-bottom:6px;">Caller Information</div>
        <div style="font-weight:700; font-size:16px;">{{ call.name }}</div>
        <div class="muted">{{ call.phone }} · {{ call.time }} · {{ call.duration }}</div>
      </div>

      <div class="card">
        <div class="row"><span class="label" style="margin:0;">Risk Analysis</span><span class="pill" :class="pillClass">{{ tagLabel }} — {{ call.riskScore }}/100</span></div>
      </div>

      <div class="card" v-if="call.keywords && call.keywords.length">
        <div class="label" style="margin-bottom:6px;">Scam Keywords</div>
        <div style="display:flex; flex-wrap:wrap; gap:6px;">
          <span class="pill pill-red" v-for="k in call.keywords" :key="k">{{ k }}</span>
        </div>
      </div>

      <div class="card">
        <div class="label" style="margin-bottom:6px;">Detection Report</div>
        <p class="muted" style="margin:0;">{{ call.report || 'No additional detection notes for this call.' }}</p>
      </div>

      <div class="card">
        <div class="row"><span class="muted">AI Confidence Score</span><span style="font-weight:800;">{{ call.confidence }}%</span></div>
      </div>

      <button class="btn btn-ghost" @click="$router.push('/help')">Report This Call</button>
    </div>

    <div class="content" v-else>
      <p class="muted">Call not found.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getCallById } from '../callLog'

const route = useRoute()
const call = computed(() => getCallById(route.params.id))

const pillClass = computed(() => {
  if (!call.value) return ''
  return { safe: 'pill-green', suspicious: 'pill-amber', scam: 'pill-red' }[call.value.tag]
})
const tagLabel = computed(() => {
  if (!call.value) return ''
  return { safe: 'Safe', suspicious: 'Suspicious', scam: 'Scam' }[call.value.tag]
})
</script>

<style scoped>
.back-arrow {
  background: none;
  border: none;
  color: var(--navy);
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: opacity 0.15s ease;
}
.back-arrow:hover { opacity: 0.6; }
</style>