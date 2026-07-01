<!-- DAY 7 -->
<template>
  <div class="page">
    <div class="topbar"><h2>Emergency Contacts</h2><span style="width:36px;"></span></div>
    <div class="content">
      <div class="card" v-for="c in contacts" :key="c.name" style="margin-bottom:10px;">
        <div class="row">
          <div>
            <div style="font-weight:700;">{{ c.name }}</div>
            <div class="muted">{{ c.phone }} · {{ c.relation }}</div>
          </div>
          <div style="display:flex; gap:8px;">
            <button class="back" @click="edit(c)">✎</button>
            <button class="back" @click="remove(c)">🗑</button>
          </div>
        </div>
      </div>

      <div class="card" v-if="showAdd">
        <input class="field" v-model="newContact.name" placeholder="Contact name" />
        <input class="field" v-model="newContact.phone" placeholder="Phone number" />
        <input class="field" v-model="newContact.relation" placeholder="Relation (e.g. Daughter)" />
        <button class="btn btn-primary" @click="addContact">Save Contact</button>
      </div>

      <button class="btn btn-gold" @click="showAdd = !showAdd">{{ showAdd ? 'Cancel' : '+ Add Contact' }}</button>
    </div>
    <AppShell active="contacts" />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import AppShell from '../components/AppShell.vue'
const contacts = ref([
  { name:'Riya Gupta', phone:'+91 98xxx xx001', relation:'Daughter' },
  { name:'Aman Gupta', phone:'+91 98xxx xx002', relation:'Son' },
])
const showAdd = ref(false)
const newContact = reactive({ name:'', phone:'', relation:'' })
function addContact(){
  if(!newContact.name) return
  contacts.value.push({ ...newContact })
  newContact.name = ''; newContact.phone=''; newContact.relation=''
  showAdd.value = false
}
function edit(c){ /* wire up to an edit form as needed */ }
function remove(c){ contacts.value = contacts.value.filter(x => x !== c) }
</script>
