<template>
  <div class="page">
    <div class="topbar">
      <button class="back-arrow" @click="$router.back()" aria-label="Go back">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M15 18l-6-6 6-6" />
        </svg>
      </button>
      <h2>Family Alert</h2>
      <span style="width:36px;"></span>
    </div>

    <div class="content" style="display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding-top:20px;">

      <!-- Sending state -->
      <template v-if="status === 'sending'">
        <div style="width:80px;height:80px;border-radius:50%; background:rgba(224,165,38,0.15); border:2px solid var(--amber); display:flex;align-items:center;justify-content:center; font-size:32px; margin-bottom:18px;">
          <div style="width:28px;height:28px;border:3px solid rgba(224,165,38,0.3); border-top-color:var(--amber); border-radius:50%; animation:spin 0.8s linear infinite;"></div>
        </div>
        <h2>Alerting Your Family…</h2>
        <p class="muted" style="margin:8px 0 0;">Sending to {{ contacts.length }} contact{{ contacts.length === 1 ? '' : 's' }}</p>
      </template>

      <!-- Sent state -->
      <template v-else>
        <div style="width:80px;height:80px;border-radius:50%; background:rgba(47,158,104,0.12); border:2px solid var(--green); display:flex;align-items:center;justify-content:center; font-size:32px; margin-bottom:18px;">✅</div>
        <h2>Alert Successfully Sent</h2>
        <p class="muted" style="margin:8px 0 22px;">
          {{ contacts.length }} emergency contact{{ contacts.length === 1 ? '' : 's' }} notified about this call.
        </p>

        <div class="card" style="width:100%; text-align:left;" v-for="c in contacts" :key="c.id">
          <div class="row">
            <div>
              <div style="font-weight:700;">{{ c.name }}</div>
              <div class="muted">{{ c.relation }} · Notified</div>
            </div>
            <span class="pill pill-green">Delivered</span>
          </div>
          <div class="divider"></div>
          <div class="row">
            <div class="muted">Sent at {{ time }} · Encrypted channel</div>
            <button class="btn btn-ghost" style="width:auto; padding:8px 14px; margin:0; font-size:13px;" @click="startCall(c)">📞 Call {{ c.name.split(' ')[0] }}</button>
          </div>
        </div>

        <button class="btn btn-primary" style="margin-top:8px;" @click="$router.push('/dashboard')">Return Home</button>
      </template>

    </div>

    <!-- Calling overlay -->
    <div v-if="callingContact" style="position:fixed; inset:0; background:rgba(27,42,74,0.55); display:flex; align-items:center; justify-content:center; z-index:50;" @click.self="cancelCall">
      <div style="background:var(--card); border-radius:20px; padding:32px 28px; width:280px; text-align:center; box-shadow:0 20px 50px rgba(0,0,0,0.3);">
        <div style="width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#8A93A8,#4A5A73); margin:0 auto 16px; display:flex;align-items:center;justify-content:center; color:#fff; font-size:26px; font-weight:700;">
          {{ callingContact.name.charAt(0) }}
        </div>
        <div style="font-weight:800; font-size:16px; margin-bottom:2px;">{{ callingContact.name }}</div>
        <div class="muted" style="margin-bottom:6px;">{{ callingContact.phone }}</div>
        <div style="color:var(--amber); font-weight:700; font-size:13px; margin-bottom:22px;">Calling…</div>
        <div style="display:flex; justify-content:center;">
          <button @click="cancelCall" style="width:52px;height:52px;border-radius:50%;background:var(--red); border:none; color:#fff; font-size:20px;">✕</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const status = ref('sending')
const contacts = ref([])
const time = new Date().toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' })

const callingContact = ref(null)

function loadContacts() {
  const saved = localStorage.getItem('digitalBodyguard.contacts')
  if (saved) {
    contacts.value = JSON.parse(saved)
  } else {
    contacts.value = [
      { id: 1, name: 'Riya Gupta', phone: '+919800000001', relation: 'Daughter' }
    ]
  }
}

function startCall(contact) {
  callingContact.value = contact
  window.location.href = 'tel:' + contact.phone.replace(/\s/g, '')
}

function cancelCall() {
  callingContact.value = null
}

onMounted(() => {
  loadContacts()
  setTimeout(() => {
    status.value = 'sent'
  }, 1200)
})
</script>

<style scoped>
@keyframes spin { to { transform: rotate(360deg); } }
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
</style>