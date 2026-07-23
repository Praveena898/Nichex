<template>
  <div class="page" style="align-items:center; justify-content:center; background:var(--navy);">
    <div style="text-align:center; color:#fff;">
      <svg width="88" height="88" viewBox="0 0 64 64" style="margin-bottom:18px;">
        <path d="M32 4 L56 14 V30 C56 46 46 56 32 60 C18 56 8 46 8 30 V14 Z" fill="none" stroke="#F7F3EC" stroke-width="3"/>
        <path d="M22 32 L29 39 L43 24" fill="none" stroke="#2F9E68" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <h1 style="color:#fff; font-size:24px; letter-spacing:0.5px;">{{ t('splash.name') }}</h1>
      <p style="color:#B7BFCF; font-size:13px; margin-top:6px;">{{ t('splash.tagline') }}</p>
      <div class="loader" style="margin:36px auto 0; width:34px; height:34px; border:3px solid rgba(255,255,255,0.25); border-top-color:#C9A227; border-radius:50%; animation: spin 0.9s linear infinite;"></div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { t } from '../i18n'
const router = useRouter()
onMounted(() => {
  setTimeout(() => router.push('/onboarding'), 1400)
})
</script>

<style scoped>
@keyframes spin { to { transform: rotate(360deg); } }
</style>