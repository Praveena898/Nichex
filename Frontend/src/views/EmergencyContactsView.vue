<template>
  <div class="page">
    <div class="topbar"><h2>{{ t('contacts.title') }}</h2><span style="width:36px;"></span></div>
    <div class="content">
      <div class="card" v-for="c in contacts" :key="c.id" style="margin-bottom:10px;">
        <div class="row">
          <div>
            <div style="font-weight:700;">{{ c.name }}</div>
            <div class="muted">{{ c.phone }} · {{ c.relation }}</div>
          </div>
          <div style="display:flex; gap:8px;">
            <button class="icon-btn" @click="startEdit(c)" aria-label="Edit contact">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 20h9"/>
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4Z"/>
              </svg>
            </button>
            <button class="icon-btn" @click="remove(c)" aria-label="Delete contact">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 6h18"/>
                <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                <path d="M10 11v6"/><path d="M14 11v6"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div class="card" v-if="showAdd">
        <input class="field" v-model="form.name" :placeholder="t('contacts.namePlaceholder')" />

        <input class="field" v-model="form.phone" :placeholder="t('contacts.phonePlaceholder')" :style="phoneError ? 'border-color:var(--red);' : ''" />
        <div v-if="phoneError" style="color:var(--red); font-size:12px; margin:-6px 0 12px;">{{ phoneError }}</div>

        <input class="field" v-model="form.relation" :placeholder="t('contacts.relationPlaceholder')" />
        <div v-if="nameError" style="color:var(--red); font-size:12px; margin:-6px 0 12px;">{{ nameError }}</div>

        <button class="btn btn-primary" @click="saveContact">{{ editingId ? t('contacts.updateContact') : t('contacts.saveContact') }}</button>
      </div>

      <button class="btn btn-gold" @click="toggleAdd">{{ showAdd ? t('contacts.cancel') : t('contacts.addContact') }}</button>
    </div>
    <AppShell active="contacts" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import AppShell from '../components/AppShell.vue'
import { t } from '../i18n'

const STORAGE_KEY = 'digitalBodyguard.contacts'

const contacts = ref([])
const showAdd = ref(false)
const editingId = ref(null)
const phoneError = ref('')
const nameError = ref('')

const form = reactive({ name:'', phone:'', relation:'' })

function loadContacts() {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    contacts.value = JSON.parse(saved)
  } else {
    contacts.value = [
      { id: 1, name:'Riya Gupta', phone:'+91 98xxx xx001', relation:'Daughter' },
      { id: 2, name:'Aman Gupta', phone:'+91 98xxx xx002', relation:'Son' },
    ]
  }
}

function persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(contacts.value))
}

function resetForm() {
  form.name = ''; form.phone = ''; form.relation = ''
  phoneError.value = ''
  nameError.value = ''
  editingId.value = null
}

function toggleAdd() {
  if (showAdd.value) {
    resetForm()
  }
  showAdd.value = !showAdd.value
}

function startEdit(c) {
  form.name = c.name
  form.phone = c.phone
  form.relation = c.relation
  editingId.value = c.id
  showAdd.value = true
}

function validate() {
  phoneError.value = ''
  nameError.value = ''

  if (!form.name.trim()) {
    nameError.value = 'Please enter a name.'
  }

  const digitsOnly = form.phone.replace(/\D/g, '')
  if (digitsOnly.length < 10) {
    phoneError.value = `Phone number needs at least 10 digits (currently ${digitsOnly.length}).`
  }

  return !phoneError.value && !nameError.value
}

function saveContact() {
  if (!validate()) return

  if (editingId.value) {
    const target = contacts.value.find(c => c.id === editingId.value)
    if (target) {
      target.name = form.name
      target.phone = form.phone
      target.relation = form.relation
    }
  } else {
    contacts.value.push({
      id: Date.now(),
      name: form.name,
      phone: form.phone,
      relation: form.relation
    })
  }

  persist()
  resetForm()
  showAdd.value = false
}

function remove(c) {
  contacts.value = contacts.value.filter(x => x.id !== c.id)
  persist()
}

onMounted(loadContacts)
</script>

<style scoped>
.icon-btn{
  width:36px; height:36px; border-radius:50%;
  background: var(--ring-off);
  border: 1px solid var(--ring-off);
  color: var(--navy);
  display:flex; align-items:center; justify-content:center;
}
</style>