<!--
  Shared bottom navigation for the "logged in" part of the app.
  Drop <AppShell active="home" /> at the bottom of any dashboard-level view.
-->
<template>
  <nav class="bottomnav">
    <router-link to="/dashboard" class="navitem" :class="{active: active==='home'}">
      <span class="icon">🏠</span> Home
    </router-link>
    <router-link to="/history" class="navitem" :class="{active: active==='history'}">
      <span class="icon">📞</span> History
    </router-link>
    <router-link to="/notifications" class="navitem" :class="{active: active==='alerts'}">
      <span class="icon">🔔</span> Alerts
    </router-link>
    <router-link to="/contacts" class="navitem" :class="{active: active==='contacts'}">
      <span class="icon">👪</span> Family
    </router-link>
    <router-link to="/profile" class="navitem" :class="{active: active==='profile'}">
      <span class="icon">👤</span> Profile
    </router-link>
  </nav>
</template>

<script setup>
defineProps({ active: String })
</script>
