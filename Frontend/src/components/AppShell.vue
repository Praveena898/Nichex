<template>
  <nav class="bottomnav">
    <router-link to="/dashboard" class="navitem" :class="{active: active==='home'}">
      <span class="icon">🏠</span> {{ t('nav.home') }}
    </router-link>
    <router-link to="/history" class="navitem" :class="{active: active==='history'}">
      <span class="icon">📞</span> {{ t('nav.history') }}
    </router-link>
    <router-link to="/notifications" class="navitem" :class="{active: active==='alerts'}">
      <span class="icon">🔔</span> {{ t('nav.alerts') }}
    </router-link>
    <router-link to="/contacts" class="navitem" :class="{active: active==='contacts'}">
      <span class="icon">👪</span> {{ t('nav.contacts') }}
    </router-link>
    <router-link to="/profile" class="navitem" :class="{active: active==='profile'}">
      <span class="icon">👤</span> {{ t('nav.profile') }}
    </router-link>
  </nav>
</template>

<script setup>
import { t } from '../i18n'
defineProps({ active: String })
</script>