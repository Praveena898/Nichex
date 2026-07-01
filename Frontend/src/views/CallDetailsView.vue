<!-- DAY 6 -->
<template>
  <div class="page">
    <div class="topbar">
      <router-link to="/history" class="back">←</router-link>
      <h2>Call Details</h2>
      <span style="width:36px;"></span>
    </div>
    <div class="content">
      <div class="card">
        <div class="label" style="margin-bottom:6px;">Caller Information</div>
        <div style="font-weight:700; font-size:16px;">Unknown Number</div>
        <div class="muted">+91 98xxx xx412 · Today, 8:42 AM · 2m 14s</div>
      </div>

      <div class="card">
        <div class="row"><span class="label" style="margin:0;">Risk Analysis</span><span class="pill pill-red">Scam — 89/100</span></div>
      </div>

      <div class="card">
        <div class="label" style="margin-bottom:6px;">Scam Keywords</div>
        <div style="display:flex; flex-wrap:wrap; gap:6px;">
          <span class="pill pill-red">OTP</span>
          <span class="pill pill-red">urgent</span>
          <span class="pill pill-red">don't tell anyone</span>
        </div>
      </div>

      <div class="card">
        <div class="label" style="margin-bottom:6px;">Detection Report</div>
        <p class="muted" style="margin:0;">Synthetic voice patterns detected in the first 8 seconds. Caller requested OTP under urgency framing. Family was alerted at 8:44 AM.</p>
      </div>

      <div class="card">
        <div class="row"><span class="muted">AI Confidence Score</span><span style="font-weight:800;">94%</span></div>
      </div>

      <button class="btn btn-ghost" @click="$router.push('/help')">Report This Call</button>
    </div>
  </div>
</template>
<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>
