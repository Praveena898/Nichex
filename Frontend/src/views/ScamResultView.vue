<!-- DAY 5 -->
<template>
  <div class="page">
    <div class="content" style="display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding-top:50px;">
      <div style="width:80px;height:80px;border-radius:50%; background:rgba(214,69,69,0.12); border:2px solid var(--red); display:flex;align-items:center;justify-content:center; font-size:34px; margin-bottom:18px;">🔴</div>
      <h2 style="color:var(--red);">Scam Alert!</h2>
      <p class="muted" style="margin:10px 0 20px; padding:0 4px;">This call shows strong signs of a deepfake voice and scam pressure tactics.</p>

      <div class="card" style="width:100%; text-align:left;">
        <div class="row"><span class="muted">Risk Score</span><span style="font-weight:800; color:var(--red);">89 / 100</span></div>
        <div class="divider"></div>
        <div class="label" style="margin-bottom:6px;">Scam Keywords Detected</div>
        <div style="display:flex; flex-wrap:wrap; gap:6px;">
          <span class="pill pill-red">OTP</span>
          <span class="pill pill-red">urgent</span>
          <span class="pill pill-red">don't tell anyone</span>
          <span class="pill pill-red">bank block</span>
        </div>
      </div>

      <button class="btn btn-danger" style="margin-top:18px;" @click="$router.push('/dashboard')">End Call</button>
      <button class="btn btn-primary" style="display:flex; align-items:center; justify-content:center; gap:8px;" @click="$router.push('/family-alert')"><Icon name="alert-triangle" :size="16" /> Call Family</button>
    </div>
  </div>
</template>
<script setup>
import Icon from '../components/Icon.vue'
</script>