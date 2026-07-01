<!-- DAY 4 -->
<template>
  <div class="page">
    <div class="content" style="display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding-top:60px;">
      <div style="width:80px;height:80px;border-radius:50%; background:rgba(224,165,38,0.15); border:2px solid var(--amber); display:flex;align-items:center;justify-content:center; font-size:34px; margin-bottom:18px;">🟡</div>
      <h2 style="color:var(--amber);">This Call Looks Suspicious</h2>
      <p class="muted" style="margin:10px 0 20px; padding:0 8px;">Some unusual language was detected. Avoid sharing OTPs, passwords or bank details.</p>

      <div class="card" style="width:100%;">
        <div class="row"><span class="muted">Confidence Score</span><span style="font-weight:800; color:var(--amber);">61 / 100</span></div>
      </div>

      <button class="btn btn-primary" style="margin-top:18px;" @click="$router.push('/dashboard')">Continue Carefully</button>
      <button class="btn btn-ghost" @click="$router.push('/dashboard')">End Call</button>
    </div>
  </div>
</template>
<script setup></script>
