import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'splash', component: () => import('../views/SplashView.vue') },
  { path: '/onboarding', name: 'onboarding', component: () => import('../views/OnboardingView.vue') },
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') },
  { path: '/register', name: 'register', component: () => import('../views/RegisterView.vue') },
  { path: '/dashboard', name: 'dashboard', component: () => import('../views/DashboardView.vue') },
  { path: '/incoming-call', name: 'incoming-call', component: () => import('../views/IncomingCallView.vue') },
  { path: '/voice-analysis', name: 'voice-analysis', component: () => import('../views/VoiceAnalysisView.vue') },
  { path: '/result/safe', name: 'result-safe', component: () => import('../views/SafeResultView.vue') },
  { path: '/result/suspicious', name: 'result-suspicious', component: () => import('../views/SuspiciousResultView.vue') },
  { path: '/result/scam', name: 'result-scam', component: () => import('../views/ScamResultView.vue') },
  { path: '/family-alert', name: 'family-alert', component: () => import('../views/FamilyAlertView.vue') },
  { path: '/history', name: 'history', component: () => import('../views/CallHistoryView.vue') },
  { path: '/history/:id', name: 'call-details', component: () => import('../views/CallDetailsView.vue') },
  { path: '/notifications', name: 'notifications', component: () => import('../views/NotificationsView.vue') },
  { path: '/contacts', name: 'contacts', component: () => import('../views/EmergencyContactsView.vue') },
  { path: '/settings', name: 'settings', component: () => import('../views/SettingsView.vue') },
  { path: '/profile', name: 'profile', component: () => import('../views/ProfileView.vue') },
  { path: '/help', name: 'help', component: () => import('../views/HelpSupportView.vue') },
  { path: '/about', name: 'about', component: () => import('../views/AboutView.vue') },
  { path: '/logout', name: 'logout', component: () => import('../views/LogoutConfirmView.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes
})
