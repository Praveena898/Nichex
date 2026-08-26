<!-- DAY 9 -->
<template>
  <div class="page" style="align-items:center; justify-content:center;">
    <div class="content" style="display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div style="margin-bottom:12px;"><Icon name="log-out" :size="40" color="var(--navy)" :stroke-width="1.5" /></div>
      <h2>Log out of Digital Bodyguard?</h2>
      <p class="muted" style="margin:10px 0 26px;">Call protection will stop working until you log back in.</p>
      <button class="btn btn-danger" @click="$router.push('/login')">Confirm Logout</button>
      <button class="btn btn-ghost" @click="$router.push('/dashboard')">Cancel</button>
    </div>
  </div>
</template>
<script setup>
import Icon from '../components/Icon.vue'
</script>