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
        <div class="row"><span class="label" style="margin:0;">Risk Analysis</span><span class="pill" :class="call.pillClass">{{ call.tagLabel }} — {{ call.riskScore }}/100</span></div>
      </div>
      <div class="card" v-if="call.keywords.length">
        <div class="label" style="margin-bottom:6px;">Scam Keywords</div>
        <div style="display:flex; flex-wrap:wrap; gap:6px;">
          <span class="pill pill-red" v-for="k in call.keywords" :key="k">{{ k }}</span>
        </div>
      </div>
      <div class="card">
        <div class="label" style="margin-bottom:6px;">Detection Report</div>
        <p class="muted" style="margin:0;">{{ call.report }}</p>
      </div>
      <div class="card">
        <div class="row"><span class="muted">AI Confidence Score</span><span style="font-weight:800;">{{ call.confidence }}%</span></div>
      </div>
      <button class="btn btn-ghost" @click="$router.push('/family-alert')">Report This Call</button>
    </div>
    <div class="content" v-else>
      <p class="muted">Call not found.</p>
    </div>
  </div>
</template>
<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()
const allCalls = [
  {
    id: 1,
    name: 'Riya (Daughter)',
    phone: '+91 98xxx xx001',
    time: 'Today, 9:10 AM',
    duration: '3m 42s',
    tag: 'safe',
    tagLabel: 'Safe',
    pillClass: 'pill-green',
    riskScore: 4,
    confidence: 97,
    keywords: [],
    report: 'No synthetic voice patterns or scam language detected. Call matched a known, trusted contact.'
  },
  {
    id: 2,
    name: 'Unknown Number',
    phone: '+91 98xxx xx412',
    time: 'Today, 8:42 AM',
    duration: '2m 14s',
    tag: 'scam',
    tagLabel: 'Scam',
    pillClass: 'pill-red',
    riskScore: 89,
    confidence: 94,
    keywords: ['OTP', 'urgent', "don't tell anyone"],
    report: 'Synthetic voice patterns detected in the first 8 seconds. Caller requested OTP under urgency framing. Family was alerted at 8:44 AM.'
  },
  {
    id: 3,
    name: 'Bank Helpline',
    phone: '+91 1800 xxx xxx',
    time: 'Yesterday, 6:15 PM',
    duration: '5m 03s',
    tag: 'safe',
    tagLabel: 'Safe',
    pillClass: 'pill-green',
    riskScore: 8,
    confidence: 95,
    keywords: [],
    report: 'No synthetic voice patterns or scam language detected. Verified toll-free banking number.'
  },
  {
    id: 4,
    name: '+91 90xxx xx221',
    phone: '+91 90xxx xx221',
    time: 'Yesterday, 2:03 PM',
    duration: '1m 28s',
    tag: 'suspicious',
    tagLabel: 'Suspicious',
    pillClass: 'pill-amber',
    riskScore: 58,
    confidence: 81,
    keywords: ['urgent', 'verify account'],
    report: 'Some pressure language detected, but no synthetic voice patterns found. Recommend caution — do not share personal details.'
  }
]
const call = computed(() => allCalls.find(c => c.id === Number(route.params.id)))
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