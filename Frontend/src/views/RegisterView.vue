<template>
  <div class="page">
    <div class="topbar">
      <button class="back-arrow" @click="$router.back()" aria-label="Go back">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M15 18l-6-6 6-6" />
        </svg>
      </button>
      <h2>{{ t('register.title') }}</h2>
      <span style="width:36px;"></span>
    </div>
    <div class="content">
      <label class="label">{{ t('register.nameLabel') }}</label>
      <input class="field" v-model="form.name" placeholder="e.g. Ramesh Gupta" :style="errors.name ? 'border-color:var(--red);' : ''" />
      <div v-if="errors.name" class="field-error">{{ errors.name }}</div>

      <label class="label">{{ t('register.phoneLabel') }}</label>
      <input class="field" v-model="form.phone" placeholder="+91 98xxx xxxxx" :style="errors.phone ? 'border-color:var(--red);' : ''" />
      <div v-if="errors.phone" class="field-error">{{ errors.phone }}</div>

      <label class="label">{{ t('register.emailLabel') }}</label>
      <input class="field" v-model="form.email" placeholder="name@email.com" :style="errors.email ? 'border-color:var(--red);' : ''" />
      <div v-if="errors.email" class="field-error">{{ errors.email }}</div>

      <label class="label">{{ t('register.passwordLabel') }}</label>
      <div class="password-wrap">
        <input class="field" :type="showPassword ? 'text' : 'password'" v-model="form.password" placeholder="Create a password (min 6 characters)" :style="errors.password ? 'border-color:var(--red);' : ''" />
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

      <label class="label">{{ t('settings.language') }}</label>
      <select v-model="form.language" class="field">
        <option value="en">English</option>
        <option value="hi">हिन्दी (Hindi)</option>
        <option value="kok">कोंकणी (Konkani)</option>
        <option value="ml">മലയാളം (Malayalam)</option>
      </select>

      <div v-if="formError" class="field-error" style="margin-bottom:12px; margin-top:12px;">{{ formError }}</div>

      <button class="btn btn-primary" @click="handleRegister">{{ t('register.button') }}</button>
      <p class="muted" style="text-align:center;">
        {{ t('register.haveAccount') }} <router-link to="/login" style="color:var(--navy); font-weight:700;">{{ t('register.login') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { t, setLocale, locale } from '../i18n'
import { register } from '../services/api'

const router = useRouter()
const showPassword = ref(false)

const form = reactive({
  name: '', phone: '', email: '', password: '',
  language: locale.value
})

watch(() => form.language, (newLang) => {
  setLocale(newLang)
})

const errors = reactive({ name: '', phone: '', email: '', password: '' })
const formError = ref('')

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validate() {
  errors.name = ''
  errors.phone = ''
  errors.email = ''
  errors.password = ''

  if (!form.name.trim()) errors.name = 'Please enter your full name.'

  const digitsOnly = form.phone.replace(/\D/g, '')
  if (digitsOnly.length < 10) errors.phone = `Phone number needs at least 10 digits (currently ${digitsOnly.length}).`

  if (!emailPattern.test(form.email.trim())) errors.email = 'Please enter a valid email address.'

  if (form.password.length < 6) errors.password = 'Password must be at least 6 characters.'

  return !errors.name && !errors.phone && !errors.email && !errors.password
}

async function handleRegister() {
  formError.value = ''

  if (!validate()) return

  try {
    const user = await register({
      name: form.name,
      email: form.email.trim().toLowerCase(),
      password: form.password,
      phone: form.phone
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

    localStorage.setItem('digitalBodyguard.loggedIn', '1')
    localStorage.setItem('digitalBodyguard.userId', user.id)

    setLocale(form.language)

    router.push('/dashboard')
  } catch (err) {
    formError.value =
      err.response?.data?.detail ||
      'Registration failed.'
  }
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