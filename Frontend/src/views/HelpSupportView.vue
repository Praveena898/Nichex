<!-- DAY 9 -->
<template>
  <div class="page">
    <div class="topbar">
      <router-link to="/dashboard" class="back"><Icon name="arrow-left" :size="18" /></router-link>
      <h2>Help &amp; Support</h2>
      <span style="width:36px;"></span>
    </div>
    <div class="content">
      <div class="label">FAQs</div>
      <div class="card" v-for="f in faqs" :key="f.q" style="margin-bottom:8px;">
        <div style="font-weight:700; font-size:13.5px;">{{ f.q }}</div>
        <div class="muted" style="margin-top:4px;">{{ f.a }}</div>
      </div>

      <div class="divider"></div>
      <button class="btn btn-danger" style="display:flex; align-items:center; justify-content:center; gap:8px;" @click="$router.push('/help')"><Icon name="flag" :size="16" /> Report a Scam Call</button>
      <button class="btn btn-ghost" style="display:flex; align-items:center; justify-content:center; gap:8px;"><Icon name="mail" :size="16" /> Contact Support</button>
    </div>
  </div>
</template>
<script setup>
import Icon from '../components/Icon.vue'
const faqs = [
  { q:'How does the app detect scams?', a:'It listens for AI-generated voice patterns and common scam phrases like OTP requests.' },
  { q:'Is my call audio stored?', a:'No — analysis happens on your device and audio is not saved without your permission.' },
]
</script>