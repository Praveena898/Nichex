<!-- DAY 8 -->
<template>
  <div class="page">
    <div class="topbar"><h2>Profile</h2><router-link to="/settings" class="back">⚙️</router-link></div>
    <div class="content">
      <div style="text-align:center; margin-bottom:20px;">
        <div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#8A93A8,#4A5A73); margin:0 auto 10px; display:flex;align-items:center;justify-content:center; color:#fff; font-size:26px; font-weight:700;">R</div>
        <div style="font-weight:800; font-size:17px;">Ramesh Gupta</div>
        <div class="muted">Member since Jan 2026</div>
      </div>

      <div class="row" style="margin-bottom:6px;">
        <div class="label" style="margin:0;">User Details</div>
        <button class="icon-btn" @click="toggleEdit" aria-label="Edit user details">
          <svg v-if="!editing" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9"/>
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4Z"/>
          </svg>
          <span v-else style="font-size:12px; font-weight:700;">✕</span>
        </button>
      </div>

      <div class="card" v-if="!editing">
        <div class="row" style="margin-bottom:8px;"><span class="muted">Phone</span><span>{{ savedPhone }}</span></div>
        <div class="row"><span class="muted">Email</span><span>{{ savedEmail }}</span></div>
      </div>

      <div class="card" v-else>
        <label class="label">Phone</label>
        <input class="field" v-model="form.phone" placeholder="+91 98xxx xxxxx" :style="phoneError ? 'border-color:var(--red);' : ''" />
        <div v-if="phoneError" style="color:var(--red); font-size:12px; margin:-6px 0 12px;">{{ phoneError }}</div>

        <label class="label">Email</label>
        <input class="field" v-model="form.email" placeholder="name@email.com" :style="emailError ? 'border-color:var(--red);' : ''" />
        <div v-if="emailError" style="color:var(--red); font-size:12px; margin:-6px 0 12px;">{{ emailError }}</div>

        <button class="btn btn-primary" style="margin-top:4px;" @click="saveDetails">Save Changes</button>
      </div>

      <div class="label">Emergency Contacts</div>
      <div class="card row" style="cursor:pointer;" @click="$router.push('/contacts')">
        <span>2 contacts saved</span><span class="muted">›</span>
      </div>

      <div class="label">Account Information</div>
      <div class="card">
        <div class="row"><span class="muted">Plan</span><span class="pill pill-green">Protected</span></div>
      </div>
    </div>
    <AppShell active="profile" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import AppShell from '../components/AppShell.vue'

const STORAGE_KEY = 'digitalBodyguard.profile'

const savedPhone = ref('+91 98xxx xx000')
const savedEmail = ref('ramesh@email.com')

const editing = ref(false)
const phoneError = ref('')
const emailError = ref('')
const form = reactive({ phone: '', email: '' })

function loadProfile() {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    const data = JSON.parse(saved)
    savedPhone.value = data.phone
    savedEmail.value = data.email
  }
}

function toggleEdit() {
  if (!editing.value) {
    form.phone = savedPhone.value
    form.email = savedEmail.value
    phoneError.value = ''
    emailError.value = ''
  }
  editing.value = !editing.value
}

function validate() {
  phoneError.value = ''
  emailError.value = ''

  const digitsOnly = form.phone.replace(/\D/g, '')
  if (digitsOnly.length < 10) {
    phoneError.value = `Phone number needs at least 10 digits (currently ${digitsOnly.length}).`
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailPattern.test(form.email.trim())) {
    emailError.value = 'Please enter a valid email address.'
  }

  return !phoneError.value && !emailError.value
}

function saveDetails() {
  if (!validate()) return
  savedPhone.value = form.phone
  savedEmail.value = form.email
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ phone: savedPhone.value, email: savedEmail.value }))
  editing.value = false
}

onMounted(loadProfile)
</script>

<style scoped>
.icon-btn{
  width:30px; height:30px; border-radius:50%;
  background: var(--ring-off);
  border: 1px solid var(--ring-off);
  color: var(--navy);
  display:flex; align-items:center; justify-content:center;
}
</style>