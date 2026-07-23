<template>
  <div class="page">
    <div class="content" style="padding-top:30px;">
      <div style="text-align:center;">
        <div class="risk-ring" style="width:150px;height:150px;border-radius:50%; margin:0 auto 16px; background:radial-gradient(circle,rgba(224,165,38,0.15),transparent 70%); box-shadow:0 0 0 8px rgba(224,165,38,0.18); display:flex;align-items:center;justify-content:center;">
          <div style="width:118px;height:118px;border-radius:50%;background:var(--card); display:flex;flex-direction:column;align-items:center;justify-content:center;">
            <div style="font-weight:800; font-size:15px;">ANALYZING…</div>
            <div class="muted" style="font-size:10.5px; margin-top:2px;">{{ progress }}%</div>
          </div>
        </div>
        <p class="muted">Live scanning in progress</p>
      </div>

      <div class="card" style="margin-top:20px;">
        <div class="row"><span>🎙️ Voice Pattern Analysis</span><span class="pill pill-amber">Checking…</span></div>
      </div>
      <div class="card">
        <div class="row"><span>🧠 Scam Language Detection</span><span class="pill pill-amber">Checking…</span></div>
      </div>
      <div class="card">
        <div class="row"><span>📊 AI Detection Progress</span><span class="muted">{{ progress }}%</span></div>
        <div style="height:8px; background:var(--ring-off); border-radius:6px; margin-top:8px; overflow:hidden;">
          <div :style="{width:progress+'%', height:'100%', background:'var(--navy)', transition:'width .3s'}"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { addCall } from '../callLog'

const router = useRouter()
const progress = ref(0)

onMounted(() => {
  const t = setInterval(() => {
    progress.value += 20
    if (progress.value >= 100) {
      clearInterval(t)
      setTimeout(() => {
        const entry = addCall({
          name: 'Unknown Number',
          phone: '+91 98xxx xx412',
          tag: 'scam',
          riskScore: 89,
          confidence: 94,
          keywords: ['OTP', 'urgent', "don't tell anyone"],
          report: 'Synthetic voice patterns detected in the first 8 seconds. Caller requested OTP under urgency framing.',
          duration: '2m 14s'
        })
        router.push('/result/scam?callId=' + entry.id)
      }, 400)
    }
  }, 400)
})
</script>