<template>
  <div class="page">
    <div class="topbar">
      <button class="back-arrow" @click="$router.push('/login')" aria-label="Go back">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M15 18l-6-6 6-6" />
        </svg>
      </button>
      <h2>Reset Password</h2>
      <span style="width:36px;"></span>
    </div>

    <div class="content" style="padding-top:10px;">

      <!-- Step 1: verify email -->
      <template v-if="step === 'verify'">
        <p class="muted" style="margin-bottom:22px;">Enter the email you registered with to reset your password.</p>

        <label class="label">Email</label>
        <input class="field" v-model="email" placeholder="name@email.com" :style="verifyError ? 'border-color:var(--red);' : ''" />
        <div v-if="verifyError" class="field-error">{{ verifyError }}</div>

        <button class="btn btn-primary" @click="verifyEmail">Continue</button>
      </template>

      <!-- Step 2: set new password -->
      <template v-else-if="step === 'reset'">
        <p class="muted" style="margin-bottom:22px;">Choose a new password for <strong>{{ email }}</strong>.</p>

        <label class="label">New Password</label>
        <input class="field" type="password" v-model="newPassword" placeholder="At least 6 characters" :style="resetError ? 'border-color:var(--red);' : ''" />

        <label class="label">Confirm New Password</label>
        <input class="field" type="password" v-model="confirmPassword" placeholder="Re-enter password" :style="resetError ? 'border-color:var(--red);' : ''" />
        <div v-if="resetError" class="field-error">{{ resetError }}</div>

        <button class="btn btn-primary" @click="resetPassword">Reset Password</button>
      </template>

      <!-- Step 3: success -->
      <template v-else>
        <div style="text-align:center; padding-top:30px;">
          <div style="width:70px;height:70px;border-radius:50%; background:rgba(47,158,104,0.12); border:2px solid var(--green); display:flex;align-items:center;justify-content:center; font-size:28px; margin:0 auto 18px;">✅</div>
          <h2>Password Updated</h2>
          <p class="muted" style="margin:8px 0 24px;">You can now log in with your new password.</p>
          <button class="btn btn-primary" @click="$router.push('/login')">Go to Login</button>
        </div>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const step = ref('verify')
const email = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const verifyError = ref('')
const resetError = ref('')

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function verifyEmail() {
  verifyError.value = ''

  if (!emailPattern.test(email.value.trim())) {
    verifyError.value = 'Please enter a valid email address.'
    return
  }

  const saved = localStorage.getItem('digitalBodyguard.account')
  if (!saved) {
    verifyError.value = 'No account found. Please create an account first.'
    return
  }

  const account = JSON.parse(saved)
  if (account.email !== email.value.trim().toLowerCase()) {
    verifyError.value = 'No account found with that email.'
    return
  }

  step.value = 'reset'
}

function resetPassword() {
  resetError.value = ''

  if (newPassword.value.length < 6) {
    resetError.value = 'Password must be at least 6 characters.'
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    resetError.value = 'Passwords do not match.'
    return
  }

  const saved = localStorage.getItem('digitalBodyguard.account')
  const account = JSON.parse(saved)
  account.password = newPassword.value
  localStorage.setItem('digitalBodyguard.account', JSON.stringify(account))

  step.value = 'done'
}
</script>

<style scoped>
.back-arrow {
  background: none;
  border: none;
  color: var(--navy);
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: opacity 0.15s ease;
}
.back-arrow:hover { opacity: 0.6; }
.field-error {
  color: var(--red);
  font-size: 12px;
  margin: -6px 0 12px;
}
</style>