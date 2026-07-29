<template>
  <div class="page">
    <div class="topbar">
      <button class="back-arrow" @click="$router.back()" aria-label="Go back">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M15 18l-6-6 6-6" />
        </svg>
      </button>
      <h2>{{ t('login.title') }}</h2>
      <span style="width:36px;"></span>
    </div>

    <div class="content" style="padding-top:20px;">
      <p class="muted" style="margin-bottom:26px;">{{ t('login.subtitle') }}</p>

      <label class="label">{{ t('login.emailLabel') }}</label>
      <input class="field" v-model="email" placeholder="e.g. name@email.com" :style="errors.email ? 'border-color:var(--red);' : ''" />
      <div v-if="errors.email" class="field-error">{{ errors.email }}</div>

      <label class="label">{{ t('login.passwordLabel') }}</label>
      <input class="field" type="password" v-model="password" placeholder="••••••••" :style="errors.password ? 'border-color:var(--red);' : ''" />
      <div v-if="errors.password" class="field-error">{{ errors.password }}</div>

      <div class="row" style="margin-bottom:20px;">
        <label class="muted"><input type="checkbox" /> {{ t('login.remember') }}</label>
        <router-link to="/forgot-password" class="muted" style="text-decoration:underline;">{{ t('login.forgot') }}</router-link>
      </div>

      <div v-if="formError" class="field-error" style="margin-bottom:12px;">{{ formError }}</div>

      <button class="btn btn-primary" @click="handleLogin">{{ t('login.button') }}</button>
      <p class="muted" style="text-align:center; margin-top:14px;">
        {{ t('login.noAccount') }} <router-link to="/register" style="color:var(--navy); font-weight:700;">{{ t('login.createAccount') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { t } from '../i18n'

const router = useRouter()
const email = ref('')
const password = ref('')
const errors = reactive({ email: '', password: '' })
const formError = ref('')

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validate() {
  errors.email = ''
  errors.password = ''

  if (!emailPattern.test(email.value.trim())) errors.email = 'Please enter a valid email address.'
  if (!password.value) errors.password = 'Please enter your password.'

  return !errors.email && !errors.password
}

function handleLogin() {
  formError.value = ''
  if (!validate()) return

  const saved = localStorage.getItem('digitalBodyguard.account')
  if (!saved) {
    formError.value = 'No account found. Please create an account first.'
    return
  }

  const account = JSON.parse(saved)
  const enteredEmail = email.value.trim().toLowerCase()

  if (enteredEmail !== account.email || password.value !== account.password) {
    formError.value = 'Incorrect email or password. Please try again.'
    return
  }

  localStorage.setItem('digitalBodyguard.loggedIn', '1')
  router.push('/dashboard')
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