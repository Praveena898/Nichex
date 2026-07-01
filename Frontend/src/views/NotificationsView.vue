<!-- DAY 7 -->
<template>
  <div class="page">
    <div class="topbar"><h2>Notifications</h2><span style="width:36px;"></span></div>
    <div class="content">
      <div class="label">Scam Alerts</div>
      <div class="card" style="border-left:4px solid var(--red); margin-bottom:10px;">
        <div style="font-weight:700;">🔴 Scam call detected</div>
        <div class="muted">Unknown Number · Today, 8:42 AM</div>
      </div>

      <div class="label">Family Notifications</div>
      <div class="card" style="border-left:4px solid var(--green); margin-bottom:10px;">
        <div style="font-weight:700;">✅ Alert sent to Riya</div>
        <div class="muted">Delivered · Today, 8:44 AM</div>
      </div>

      <div class="label">Security Updates</div>
      <div class="card" style="border-left:4px solid var(--navy); margin-bottom:10px;">
        <div style="font-weight:700;">🔒 Detection model updated</div>
        <div class="muted">New scam-phrase patterns added · Yesterday</div>
      </div>
    </div>
    <AppShell active="alerts" />
  </div>
</template>
<script setup>
import AppShell from '../components/AppShell.vue'
</script>
