<template>
  <div class="page">
    <div class="topbar"><h2>{{ t('profile.title') }}</h2><router-link to="/settings" class="back"><Icon name="settings" :size="18" /></router-link></div>
    <div class="content">
      <div style="text-align:center; margin-bottom:20px;">
        <div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#8A93A8,#4A5A73); margin:0 auto 10px; display:flex;align-items:center;justify-content:center; color:#fff; font-size:26px; font-weight:700;">{{ initial }}</div>
        <div style="font-weight:800; font-size:17px;">{{ fullName }}</div>
        <div class="muted">{{ t('profile.memberSince') }}</div>
      </div>

      <div class="row" style="margin-bottom:6px;">
        <div class="label" style="margin:0;">{{ t('profile.userDetails') }}</div>
        <button class="icon-btn" @click="toggleEdit" aria-label="Edit user details">
          <svg v-if="!editing" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9"/>
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4Z"/>
          </svg>
          <Icon v-else name="x" :size="15" />
        </button>
      </div>

      <div class="card" v-if="!editing">
        <div class="row" style="margin-bottom:8px;"><span class="muted">{{ t('profile.phone') }}</span><span>{{ account.phone || '—' }}</span></div>
        <div class="row"><span class="muted">{{ t('profile.email') }}</span><span>{{ account.email || '—' }}</span></div>
      </div>

      <div class="card" v-else>
        <label class="label">{{ t('profile.phone') }}</label>
        <input class="field" v-model="form.phone" placeholder="+91 98xxx xxxxx" :style="phoneError ? 'border-color:var(--red);' : ''" />
        <div v-if="phoneError" style="color:var(--red); font-size:12px; margin:-6px 0 12px;">{{ phoneError }}</div>

        <label class="label">{{ t('profile.email') }}</label>
        <input class="field" v-model="form.email" placeholder="name@email.com" :style="emailError ? 'border-color:var(--red);' : ''" />
        <div v-if="emailError" style="color:var(--red); font-size:12px; margin:-6px 0 12px;">{{ emailError }}</div>

        <button class="btn btn-primary" style="margin-top:4px;" @click="saveDetails">{{ t('profile.saveChanges') }}</button>
      </div>

      <div class="label">{{ t('profile.emergencyContacts') }}</div>
      <div class="card row" style="cursor:pointer;" @click="$router.push('/contacts')">
        <span>{{ contactsCount }} {{ contactsCount === 1 ? t('profile.contactSaved') : t('profile.contactsSaved') }}</span><span class="muted">›</span>
      </div>

      <div class="label">{{ t('profile.accountInformation') }}</div>
      <div class="card">
        <div class="row"><span class="muted">{{ t('profile.plan') }}</span><span class="pill pill-green">{{ t('profile.protectedLabel') }}</span></div>
      </div>
    </div>
    <AppShell active="profile" />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import AppShell from '../components/AppShell.vue'
import { t } from '../i18n'
import Icon from '../components/Icon.vue'

const ACCOUNT_KEY = 'digitalBodyguard.account'

const account = ref({ name: '', phone: '', email: '' })
const contactsCount = ref(0)

const fullName = computed(() => account.value.name || 'Your Name')
const initial = computed(() => (account.value.name || 'U').charAt(0).toUpperCase())

const editing = ref(false)
const phoneError = ref('')
const emailError = ref('')
const form = reactive({ phone: '', email: '' })

function loadAccount() {
  const saved = localStorage.getItem(ACCOUNT_KEY)
  if (saved) {
    account.value = JSON.parse(saved)
  }

  const savedContacts = localStorage.getItem('digitalBodyguard.contacts')
  if (savedContacts) {
    contactsCount.value = JSON.parse(savedContacts).length
  }
}

function toggleEdit() {
  if (!editing.value) {
    form.phone = account.value.phone || ''
    form.email = account.value.email || ''
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

  account.value.phone = form.phone
  account.value.email = form.email.trim().toLowerCase()
  localStorage.setItem(ACCOUNT_KEY, JSON.stringify(account.value))

  editing.value = false
}

onMounted(loadAccount)
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