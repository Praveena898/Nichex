<!-- DAY 4 -->
<template>
  <div class="page">
    <div class="content" style="display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding-top:60px;">
      <div style="width:80px;height:80px;border-radius:50%; background:rgba(47,158,104,0.12); border:2px solid var(--green); display:flex;align-items:center;justify-content:center; font-size:34px; margin-bottom:18px;">🟢</div>
      <h2 style="color:var(--green);">This Call Looks Safe</h2>
      <p class="muted" style="margin:10px 0 26px;">No scam signals or synthetic voice patterns were detected.</p>

      <div class="card" style="width:100%;">
        <div class="row"><span class="muted">Confidence Score</span><span style="font-weight:800; color:var(--green);">96 / 100</span></div>
      </div>

      <button class="btn btn-success" style="margin-top:18px;" @click="$router.push('/dashboard')">Continue Call</button>
    </div>
  </div>
</template>
<script setup></script>
