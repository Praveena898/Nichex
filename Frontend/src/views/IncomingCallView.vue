<!-- DAY 3 -->
<template>
  <div class="page" style="background:var(--navy); color:#fff; align-items:center; justify-content:center;">
    <div style="position:absolute; top:20px; right:20px;" class="pill" style="background:rgba(255,255,255,0.12); color:#fff;">🛡️ AI Protection Enabled</div>
    <div style="text-align:center;">
      <div style="width:100px;height:100px;border-radius:50%;background:linear-gradient(135deg,#8A93A8,#4A5A73); display:flex;align-items:center;justify-content:center; font-size:36px; font-weight:700; margin:0 auto 18px;">?</div>
      <h2 style="color:#fff;">Unknown Caller</h2>
      <p style="color:#B7BFCF; margin-top:4px;">+91 98xxx xx412</p>
      <p style="color:#8B93A6; font-size:12px; margin-top:24px;">Guardian is scanning this call…</p>
    </div>
    <div style="display:flex; gap:50px; margin-top:60px;">
      <button @click="$router.push('/dashboard')" style="width:60px;height:60px;border-radius:50%;background:var(--red); border:none; color:#fff; font-size:22px;">✕</button>
      <button @click="$router.push('/voice-analysis')" style="width:60px;height:60px;border-radius:50%;background:var(--green); border:none; color:#fff; font-size:22px;">✓</button>
    </div>
  </div>
</template>

<script setup>
</script>
