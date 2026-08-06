<template>
  <div class="page">
    <div class="topbar">
      <span style="width:36px;"></span>
      <h2>{{ t('login.title') }}</h2>
      <span style="width:36px;"></span>
    </div>

    <div class="content" style="padding-top:20px;">
      <p class="muted" style="margin-bottom:26px;">{{ t('login.subtitle') }}</p>

      <label class="label">{{ t('login.emailLabel') }}</label>
      <input class="field" v-model="email" placeholder="e.g. name@email.com" :style="errors.email ? 'border-color:var(--red);' : ''" />
      <div v-if="errors.email" class="field-error">{{ errors.email }}</div>

      <label class="label">{{ t('login.passwordLabel') }}</label>
      <div class="password-wrap">
        <input class="field" :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="••••••••" :style="errors.password ? 'border-color:var(--red);' : ''" />
        <button type="button" class="eye-btn" @click="showPassword = !showPassword" :aria-label="showPassword ? 'Hide password' : 'Show password'">
          <svg v-if="!showPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8Z"/><circle cx="12" cy="12" r="3"/>
          </svg>
          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17.94 17.94A10.94 10.94 0 0 1 12 20c-7 0-11-8-11-8a18.6 18.6 0 0 1 4.22-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19M14.12 14.12a3 3 0 1 1-4.24-4.24"/>
            <path d="M1 1l22 22"/>
          </svg>
        </button>
      </div>
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
import { t, setLocale } from '../i18n'
import { login } from '../services/api'

const router = useRouter()
const email = ref('')
const password = ref('')
const showPassword = ref(false)
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

async function handleLogin() {
  formError.value = ''

  if (!validate()) return

  try {
    const user = await login({
      email: email.value.trim().toLowerCase(),
      password: password.value
    })

    localStorage.setItem(
  'digitalBodyguard.account',
  JSON.stringify({
    id: user.id,
    name: user.name,
    email: user.email,
    phone: user.phone
  })
)

    // Save only session info
    localStorage.setItem('digitalBodyguard.loggedIn', '1')
    localStorage.setItem('digitalBodyguard.userId', user.id)

    router.push('/dashboard')

  } catch (err) {
    formError.value =
      err.response?.data?.detail ||
      'Incorrect email or password.'
  }
}
</script>

<style scoped>
.field-error {
  color: var(--red);
  font-size: 12px;
  margin: -6px 0 12px;
}
.password-wrap {
  position: relative;
}
.password-wrap .field {
  padding-right: 42px;
}
.eye-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--slate);
  display: flex;
  align-items: center;
  cursor: pointer;
}
.eye-btn:hover { color: var(--navy); }
</style>