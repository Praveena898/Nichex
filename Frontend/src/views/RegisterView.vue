<!-- DAY 2 -->
<template>
  <div class="page">
    <div class="topbar">
      <router-link to="/onboarding" class="back">←</router-link>
      <h2>Create Account</h2>
      <span style="width:36px;"></span>
    </div>
    <div class="content">
      <label class="label">Full Name</label>
      <input class="field" v-model="form.name" placeholder="e.g. Ramesh Gupta" />

      <label class="label">Phone Number</label>
      <input class="field" v-model="form.phone" placeholder="+91 98xxx xxxxx" />

      <label class="label">Email</label>
      <input class="field" v-model="form.email" placeholder="name@email.com" />

      <label class="label">Password</label>
      <input class="field" type="password" v-model="form.password" placeholder="Create a password" />

      <div class="divider"></div>

      <label class="label">Emergency Contact (Family)</label>
      <input class="field" v-model="form.contactName" placeholder="Contact name" />
      <input class="field" v-model="form.contactPhone" placeholder="Contact phone number" />

      <button class="btn btn-primary" @click="$router.push('/dashboard')">Create Account</button>
      <p class="muted" style="text-align:center;">
        Already have an account? <router-link to="/login" style="color:var(--navy); font-weight:700;">Log in</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
const form = reactive({ name:'', phone:'', email:'', password:'', contactName:'', contactPhone:'' })
</script>
