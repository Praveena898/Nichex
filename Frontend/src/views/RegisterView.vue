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
      <input class="field" type="password" v-model="form.password" placeholder="Create a password (min 6 characters)" :style="errors.password ? 'border-color:var(--red);' : ''" />
      <div v-if="errors.password" class="field-error">{{ errors.password }}</div>

      <div class="divider"></div>

      <label class="label">{{ t('register.contactLabel') }}</label>
      <input class="field" v-model="form.contactName" placeholder="Contact name" />
      <input class="field" v-model="form.contactPhone" placeholder="Contact phone number" />

      <div v-if="formError" class="field-error" style="margin-bottom:12px;">{{ formError }}</div>

      <button class="btn btn-primary" @click="handleRegister">{{ t('register.button') }}</button>
      <p class="muted" style="text-align:center;">
        {{ t('register.haveAccount') }} <router-link to="/login" style="color:var(--navy); font-weight:700;">{{ t('register.login') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { t } from '../i18n'

const router = useRouter()

const form = reactive({ name:'', phone:'', email:'', password:'', contactName:'', contactPhone:'' })
const errors = reactive({ name:'', phone:'', email:'', password:'' })
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

function handleRegister() {
  formError.value = ''
  if (!validate()) return

  const account = {
    name: form.name,
    phone: form.phone,
    email: form.email.trim().toLowerCase(),
    password: form.password,
    contactName: form.contactName,
    contactPhone: form.contactPhone
  }

  localStorage.setItem('digitalBodyguard.account', JSON.stringify(account))
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