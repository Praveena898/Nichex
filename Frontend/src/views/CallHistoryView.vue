<!-- DAY 6 -->
<template>
  <div class="page">
    <div class="topbar"><h2>Call History</h2><span style="width:36px;"></span></div>
    <div class="content">
      <div class="row" style="gap:8px; margin-bottom:14px;">
        <button v-for="f in filters" :key="f" class="pill" :class="active===f ? 'pill-green' : ''" :style="active!==f ? 'background:var(--card); color:var(--slate); border:1px solid var(--ring-off);' : ''" @click="active=f" style="flex:1; justify-content:center;">{{ f }}</button>
      </div>

      <router-link v-for="c in filtered" :key="c.id" :to="'/history/'+c.id" class="card" style="display:block; margin-bottom:10px;">
        <div class="row">
          <div>
            <div style="font-weight:700;">{{ c.name }}</div>
            <div class="muted">{{ c.time }}</div>
          </div>
          <span class="pill" :class="c.pillClass">{{ c.tag }}</span>
        </div>
      </router-link>
    </div>
    <AppShell active="history" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import AppShell from '../components/AppShell.vue'
const active = ref('All')
const filters = ['All', 'Safe', 'Suspicious', 'Scam']
const calls = [
  { id:1, name:'Riya (Daughter)', time:'Today, 9:10 AM', tag:'Safe', pillClass:'pill-green' },
  { id:2, name:'Unknown Number', time:'Today, 8:42 AM', tag:'Scam', pillClass:'pill-red' },
  { id:3, name:'Bank Helpline', time:'Yesterday, 6:15 PM', tag:'Safe', pillClass:'pill-green' },
  { id:4, name:'+91 90xxx xx221', time:'Yesterday, 2:03 PM', tag:'Suspicious', pillClass:'pill-amber' },
]
const filtered = computed(() => active.value==='All' ? calls : calls.filter(c=>c.tag===active.value))
</script>
