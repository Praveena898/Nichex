<!-- DAY 1 -->
<template>
  <div class="page">
    <div class="content" style="display:flex; flex-direction:column; justify-content:center; padding-top:40px;">
      <div style="text-align:center; font-size:56px; margin-bottom:8px;">{{ slides[step].emoji }}</div>
      <h2 style="text-align:center; margin-bottom:10px;">{{ slides[step].title }}</h2>
      <p class="muted" style="text-align:center; padding:0 10px;">{{ slides[step].body }}</p>

      <div style="display:flex; justify-content:center; gap:6px; margin:26px 0;">
        <span v-for="(s,i) in slides" :key="i" :style="{width:'8px',height:'8px',borderRadius:'50%',background: i===step?'var(--navy)':'var(--ring-off)'}"></span>
      </div>

      <button class="btn btn-primary" v-if="step < slides.length-1" @click="step++">Next</button>
      <button class="btn btn-primary" v-else @click="$router.push('/register')">Get Started</button>
      <button class="btn btn-ghost" @click="$router.push('/login')">I already have an account</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const step = ref(0)
const slides = [
  { emoji:'📞', title:'Every call, watched over', body:'Digital Bodyguard listens quietly in the background for signs of scams and AI-cloned voices.' },
  { emoji:'🛡️', title:'Instant colour warnings', body:'Green, yellow or red — simple signals that tell you exactly how safe a call is, in real time.' },
  { emoji:'👪', title:'Family is one tap away', body:'If something looks wrong, your family is alerted instantly — no complicated steps required.' },
]
</script>
