<!-- DAY 2 -->
<template>
  <div class="page">
    <div class="content" style="padding-top:60px;">
      <h2 style="margin-bottom:4px;">Welcome back</h2>
      <p class="muted" style="margin-bottom:26px;">Log in to keep your protection active</p>

      <label class="label">Email or Phone</label>
      <input class="field" v-model="email" placeholder="e.g. name@email.com" />

      <label class="label">Password</label>
      <input class="field" type="password" v-model="password" placeholder="••••••••" />

      <div class="row" style="margin-bottom:20px;">
        <label class="muted"><input type="checkbox" /> Remember me</label>
        <router-link to="/help" class="muted" style="text-decoration:underline;">Forgot Password?</router-link>
      </div>

      <button class="btn btn-primary" @click="$router.push('/dashboard')">Log In</button>
      <p class="muted" style="text-align:center; margin-top:14px;">
        New here? <router-link to="/register" style="color:var(--navy); font-weight:700;">Create an account</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const email = ref('')
const password = ref('')
</script>
