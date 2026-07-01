<!-- DAY 8 -->
<template>
  <div class="page">
    <div class="topbar"><h2>Profile</h2><router-link to="/settings" class="back">⚙️</router-link></div>
    <div class="content">
      <div style="text-align:center; margin-bottom:20px;">
        <div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#8A93A8,#4A5A73); margin:0 auto 10px; display:flex;align-items:center;justify-content:center; color:#fff; font-size:26px; font-weight:700;">R</div>
        <div style="font-weight:800; font-size:17px;">Ramesh Gupta</div>
        <div class="muted">Member since Jan 2026</div>
      </div>

      <div class="label">User Details</div>
      <div class="card">
        <div class="row" style="margin-bottom:8px;"><span class="muted">Phone</span><span>+91 98xxx xx000</span></div>
        <div class="row"><span class="muted">Email</span><span>ramesh@email.com</span></div>
      </div>

      <div class="label">Emergency Contacts</div>
      <div class="card row" style="cursor:pointer;" @click="$router.push('/contacts')">
        <span>2 contacts saved</span><span class="muted">›</span>
      </div>

      <div class="label">Account Information</div>
      <div class="card">
        <div class="row"><span class="muted">Plan</span><span class="pill pill-green">Protected</span></div>
      </div>
    </div>
    <AppShell active="profile" />
  </div>
</template>
<script setup>
import AppShell from '../components/AppShell.vue'
</script>
