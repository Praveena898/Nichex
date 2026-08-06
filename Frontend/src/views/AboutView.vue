<template>
  <div class="page">
    <div class="topbar">
      <router-link to="/settings" class="back">←</router-link>
      <h2>{{ t('about.title') }}</h2>
      <span style="width:36px;"></span>
    </div>
    <div class="content" style="text-align:center; padding-top:20px;">
      <h2>Digital Bodyguard</h2>
      <div class="muted" style="margin-bottom:20px;">{{ t('about.version') }}</div>

      <div class="card" style="text-align:left;">
        <p class="muted" style="margin:0;">{{ t('about.description') }}</p>
      </div>

      <div class="label" style="margin-top:16px; text-align:left;">{{ t('about.teamMembers') }}</div>
      <div class="card" style="text-align:left;">
        <div class="row" style="margin-bottom:6px;"><span>{{ t('about.frontend') }}</span><span class="muted">{{ t('about.you') }}</span></div>
        <div class="row"><span>{{ t('about.securityBackend') }}</span><span class="muted">{{ t('about.teammate') }}</span></div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { t } from '../i18n'
</script>