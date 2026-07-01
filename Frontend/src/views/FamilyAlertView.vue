<!-- DAY 5 -->
<template>
  <div class="page">
    <div class="content" style="display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding-top:60px;">
      <div style="width:80px;height:80px;border-radius:50%; background:rgba(47,158,104,0.12); border:2px solid var(--green); display:flex;align-items:center;justify-content:center; font-size:32px; margin-bottom:18px;">✅</div>
      <h2>Alert Successfully Sent</h2>
      <p class="muted" style="margin:8px 0 22px;">Your emergency contact has been notified about this call.</p>

      <div class="card" style="width:100%; text-align:left;">
        <div class="row">
          <div>
            <div style="font-weight:700;">Riya (Daughter)</div>
            <div class="muted">Family Member Notified</div>
          </div>
          <span class="pill pill-green">Delivered</span>
        </div>
        <div class="divider"></div>
        <div class="muted">Sent at {{ time }} · Encrypted channel</div>
      </div>

      <button class="btn btn-primary" style="margin-top:18px;" @click="$router.push('/dashboard')">Return Home</button>
    </div>
  </div>
</template>

<script setup>
const time = new Date().toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' })
</script>
