<template>
  <nav class="bottomnav" :class="{ 'dark-nav': isDarkMode }">
    <router-link
      to="/dashboard"
      class="navitem"
      :class="{ active: active === 'home' }"
    >
      <span class="icon">
        <svg viewBox="0 0 24 24">
          <path d="M3 11.5 12 4l9 7.5" />
          <path d="M5.5 9.5V20a1 1 0 0 0 1 1H9a1 1 0 0 0 1-1v-4.5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1V20a1 1 0 0 0 1 1h2.5a1 1 0 0 0 1-1V9.5" />
        </svg>
      </span>
      {{ t('nav.home') }}
    </router-link>

    <router-link
      to="/history"
      class="navitem"
      :class="{ active: active === 'history' }"
    >
      <span class="icon">
        <svg viewBox="0 0 24 24">
          <path d="M6.6 10.8a15.9 15.9 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 9 9 0 0 0 2.8.45 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A16 16 0 0 1 3 5a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 9 9 0 0 0 .45 2.8 1 1 0 0 1-.25 1z" />
        </svg>
      </span>
      {{ t('nav.history') }}
    </router-link>

    <router-link
      to="/notifications"
      class="navitem"
      :class="{ active: active === 'alerts' }"
    >
      <span class="icon">
        <svg viewBox="0 0 24 24">
          <path d="M6 10.5a6 6 0 1 1 12 0c0 3.2 1 5 1.6 5.8a.6.6 0 0 1-.5 1H4.9a.6.6 0 0 1-.5-1C5 15.5 6 13.7 6 10.5z" />
          <path d="M10 19a2 2 0 0 0 4 0" />
        </svg>
      </span>
      {{ t('nav.alerts') }}
    </router-link>

    <router-link
      to="/contacts"
      class="navitem"
      :class="{ active: active === 'contacts' }"
    >
      <span class="icon">
        <svg viewBox="0 0 24 24">
          <circle cx="9" cy="8" r="2.6" />
          <path d="M4 19c0-2.8 2.2-5 5-5s5 2.2 5 5" />
          <circle cx="17" cy="9" r="2" />
          <path d="M15.5 14.2c1.9.4 3.5 2 3.5 4.3" />
        </svg>
      </span>
      {{ t('nav.contacts') }}
    </router-link>

    <router-link
      to="/profile"
      class="navitem"
      :class="{ active: active === 'profile' }"
    >
      <span class="icon">
        <svg viewBox="0 0 24 24">
          <circle cx="12" cy="8" r="3.2" />
          <path d="M5.5 20c.6-3.5 3.3-6 6.5-6s5.9 2.5 6.5 6" />
        </svg>
      </span>
      {{ t('nav.profile') }}
    </router-link>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { t } from '../i18n'

defineProps({
  active: String
})

const isDarkMode = ref(
  document.documentElement.classList.contains('dark-mode')
)

let observer

onMounted(() => {
  observer = new MutationObserver(() => {
    isDarkMode.value =
      document.documentElement.classList.contains('dark-mode')
  })

  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  })
})

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<style scoped>
.bottomnav {
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: 8px;

  background: #ffffff !important;
  border-top: 1px solid #dedede !important;
}

.bottomnav.dark-nav {
  background: #0f172a !important;
  border-top-color: #0f172a !important;
}

.navitem {
  font: inherit;
  background: transparent;
  border: none;
  cursor: pointer;

  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;

  font-size: 12px;
  font-weight: 500;

  color: #8b93a8;
  text-decoration: none;
  padding: 4px 6px;
}

.navitem.active {
  color: #111827;
}

.navitem:hover {
  color: #111827;
}

.bottomnav.dark-nav .navitem {
  color: #cbd5e1;
}

.bottomnav.dark-nav .navitem.active {
  color: #ffffff;
}

.bottomnav.dark-nav .navitem:hover {
  color: #ffffff;
}

.icon {
  display: inline-flex;
  width: 26px;
  height: 26px;
}

.icon svg {
  width: 100%;
  height: 100%;

  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.navitem.active .icon svg {
  stroke-width: 2;
}
</style>