// Temporary frontend-only "auth" bridge between Register and Login.
// Stores registered accounts in localStorage so Login can validate
// against real accounts instead of accepting anything typed in.
//
// NOTE: This is a demo-only stand-in. Passwords are stored as-is in the
// browser, which is NOT secure. Once the FastAPI backend is ready, this
// whole file gets replaced by real API calls (hashing + JWT happen server-side).

const USERS_KEY = 'db_registered_users'
const SESSION_KEY = 'db_current_user'

function getUsers() {
  try {
    return JSON.parse(localStorage.getItem(USERS_KEY) || '[]')
  } catch {
    return []
  }
}

function saveUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users))
}

export function findUserByEmail(email) {
  return getUsers().find((u) => u.email.toLowerCase() === email.trim().toLowerCase())
}

export function registerUser(form) {
  const email = form.email.trim().toLowerCase()
  if (findUserByEmail(email)) {
    return { ok: false, message: 'An account with this email already exists. Try logging in instead.' }
  }
  const users = getUsers()
  users.push({
    name: form.name.trim(),
    phone: form.phone.trim(),
    email,
    password: form.password, // demo only — never store plaintext in a real app
    contactName: form.contactName?.trim() || '',
    contactPhone: form.contactPhone?.trim() || '',
  })
  saveUsers(users)
  setSession(email)
  return { ok: true }
}

export function loginUser(email, password) {
  const user = findUserByEmail(email)
  if (!user) {
    return { ok: false, message: 'No account found with that email. Please register first.' }
  }
  if (user.password !== password) {
    return { ok: false, message: 'Incorrect password. Please try again.' }
  }
  setSession(user.email)
  return { ok: true }
}

function setSession(email) {
  localStorage.setItem(SESSION_KEY, email)
}

export function getCurrentUser() {
  const email = localStorage.getItem(SESSION_KEY)
  return email ? findUserByEmail(email) : null
}

export function logout() {
  localStorage.removeItem(SESSION_KEY)
}