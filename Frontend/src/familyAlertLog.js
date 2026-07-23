// Shared family-alert history, scoped per logged-in account (same pattern as callLog.js).

function getCurrentUserKey() {
  const saved = localStorage.getItem('digitalBodyguard.account')
  if (saved) {
    const account = JSON.parse(saved)
    if (account.email) return account.email
  }
  return 'guest'
}

function storageKey() {
  return 'digitalBodyguard.familyAlerts.' + getCurrentUserKey()
}

export function loadFamilyAlerts() {
  const saved = localStorage.getItem(storageKey())
  return saved ? JSON.parse(saved) : []
}

function saveFamilyAlerts(alerts) {
  localStorage.setItem(storageKey(), JSON.stringify(alerts))
}

export function addFamilyAlert({ contactName }) {
  const alerts = loadFamilyAlerts()
  const entry = {
    id: Date.now(),
    contactName,
    time: new Date().toLocaleString([], { hour: '2-digit', minute: '2-digit' })
  }
  alerts.unshift(entry)
  saveFamilyAlerts(alerts)
  return entry
}