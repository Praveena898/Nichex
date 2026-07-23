// Shared call-history store, scoped per logged-in account.
// Each account (identified by email) gets its own call log in localStorage,
// so logging in as a different person shows a different history.

function getCurrentUserKey() {
  const saved = localStorage.getItem('digitalBodyguard.account')
  if (saved) {
    const account = JSON.parse(saved)
    if (account.email) return account.email
  }
  return 'guest'
}

function storageKey() {
  return 'digitalBodyguard.calls.' + getCurrentUserKey()
}

export function loadCalls() {
  const saved = localStorage.getItem(storageKey())
  return saved ? JSON.parse(saved) : []
}

function saveCalls(calls) {
  localStorage.setItem(storageKey(), JSON.stringify(calls))
}

// tag: 'safe' | 'suspicious' | 'scam'
export function addCall({ name, phone, tag, riskScore, confidence, keywords, report, duration }) {
  const calls = loadCalls()
  const entry = {
    id: Date.now(),
    name: name || 'Unknown Number',
    phone: phone || '+91 98xxx xxxxx',
    time: new Date().toLocaleString([], { weekday: undefined, hour: '2-digit', minute: '2-digit' }),
    duration: duration || '1m 12s',
    tag,
    riskScore,
    confidence,
    keywords: keywords || [],
    report: report || ''
  }
  calls.unshift(entry)
  saveCalls(calls)
  return entry
}

export function getCallById(id) {
  return loadCalls().find(c => c.id === Number(id))
}

export function getStats() {
  const calls = loadCalls()
  return {
    total: calls.length,
    safe: calls.filter(c => c.tag === 'safe').length,
    suspicious: calls.filter(c => c.tag === 'suspicious').length,
    scam: calls.filter(c => c.tag === 'scam').length
  }
}