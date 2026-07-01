<!-- DAY 8 -->
<template>
  <div class="page">
    <div class="topbar">
      <router-link to="/dashboard" class="back">←</router-link>
      <h2>Settings</h2>
      <span style="width:36px;"></span>
    </div>
    <div class="content">
      <div class="card"><div class="row"><span>🌙 Dark Mode</span><input type="checkbox" /></div></div>
      <div class="card"><div class="row"><span>🌐 Language</span><span class="muted">English</span></div></div>
      <div class="card"><div class="row"><span>♿ Accessibility (Large Text)</span><input type="checkbox" checked /></div></div>
      <div class="card"><div class="row"><span>🔔 Notification Settings</span><span class="muted">›</span></div></div>
      <div class="card"><div class="row"><span>🔒 Privacy Settings</span><span class="muted">›</span></div></div>
      <div class="divider"></div>
      <button class="btn btn-ghost" @click="$router.push('/about')">About This App</button>
      <button class="btn btn-danger" @click="$router.push('/logout')">Log Out</button>
    </div>
  </div>
</template>
<script setup></script>
