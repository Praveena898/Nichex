// Lightweight global language store — no extra npm packages needed.
// Any component can `import { t, locale, setLocale } from '../i18n'`
// and call t('some.key') inside its <template>.

import { ref } from 'vue'

const dictionaries = {
  en: {
    nav: { home: 'Home', history: 'History', alerts: 'Alerts', contacts: 'Family', profile: 'Profile' },
    common: { applyChanges: 'Apply Changes', applied: 'Applied ✓', cancel: 'Cancel', continueText: 'Continue' },
    splash: { name: 'Digital Bodyguard', tagline: 'Protecting every call, every day' },
    onboarding: { getStarted: 'Get Started', haveAccount: 'I already have an account', next: 'Next' },
    login: {
      title: 'Welcome back',
      subtitle: 'Log in to keep your protection active',
      emailLabel: 'Email or Phone',
      passwordLabel: 'Password',
      remember: 'Remember me',
      forgot: 'Forgot Password?',
      button: 'Log In',
      noAccount: 'New here?',
      createAccount: 'Create an account'
    },
    register: {
      title: 'Create Account',
      nameLabel: 'Full Name',
      phoneLabel: 'Phone Number',
      emailLabel: 'Email',
      passwordLabel: 'Password',
      contactLabel: 'Emergency Contact (Family)',
      button: 'Create Account',
      haveAccount: 'Already have an account?',
      login: 'Log in'
    },
    dashboard: {
      greeting: 'Good afternoon,',
      status: 'PROTECTION STATUS',
      active: 'Active & Monitoring',
      today: "Today's Activity",
      calls: 'Calls', safe: 'Safe', suspicious: 'Suspicious', scam: 'Scam',
      recent: 'Recent Calls',
      quickActions: 'Quick Actions',
      callHistory: 'Call History',
      contacts: 'Contacts',
      emergency: 'Emergency — Alert My Family'
    },
    settings: {
      title: 'Settings',
      darkMode: 'Dark Mode',
      language: 'Language',
      accessibility: 'Accessibility (Large Text)',
      notifications: 'Notification Settings',
      privacy: 'Privacy Settings',
      about: 'About This App',
      logout: 'Log Out'
    },
    history: {
      title: 'Call History',
      all: 'All', safe: 'Safe', suspicious: 'Suspicious', scam: 'Scam'
    }
  },
  hi: {
    nav: { home: 'होम', history: 'इतिहास', alerts: 'अलर्ट', contacts: 'परिवार', profile: 'प्रोफ़ाइल' },
    common: { applyChanges: 'लागू करें', applied: 'लागू हो गया ✓', cancel: 'रद्द करें', continueText: 'जारी रखें' },
    splash: { name: 'डिजिटल बॉडीगार्ड', tagline: 'हर कॉल की सुरक्षा, हर दिन' },
    onboarding: { getStarted: 'शुरू करें', haveAccount: 'मेरे पास पहले से खाता है', next: 'आगे' },
    login: {
      title: 'वापसी पर स्वागत है',
      subtitle: 'सुरक्षा जारी रखने के लिए लॉग इन करें',
      emailLabel: 'ईमेल या फ़ोन',
      passwordLabel: 'पासवर्ड',
      remember: 'मुझे याद रखें',
      forgot: 'पासवर्ड भूल गए?',
      button: 'लॉग इन करें',
      noAccount: 'नए हैं?',
      createAccount: 'खाता बनाएं'
    },
    register: {
      title: 'खाता बनाएं',
      nameLabel: 'पूरा नाम',
      phoneLabel: 'फ़ोन नंबर',
      emailLabel: 'ईमेल',
      passwordLabel: 'पासवर्ड',
      contactLabel: 'आपातकालीन संपर्क (परिवार)',
      button: 'खाता बनाएं',
      haveAccount: 'पहले से खाता है?',
      login: 'लॉग इन करें'
    },
    dashboard: {
      greeting: 'शुभ दोपहर,',
      status: 'सुरक्षा स्थिति',
      active: 'सक्रिय और निगरानी में',
      today: 'आज की गतिविधि',
      calls: 'कॉल्स', safe: 'सुरक्षित', suspicious: 'संदिग्ध', scam: 'धोखाधड़ी',
      recent: 'हाल की कॉल्स',
      quickActions: 'त्वरित कार्रवाई',
      callHistory: 'कॉल इतिहास',
      contacts: 'संपर्क',
      emergency: 'आपातकाल — परिवार को सूचित करें'
    },
    settings: {
      title: 'सेटिंग्स',
      darkMode: 'डार्क मोड',
      language: 'भाषा',
      accessibility: 'सुगम्यता (बड़ा टेक्स्ट)',
      notifications: 'सूचना सेटिंग्स',
      privacy: 'गोपनीयता सेटिंग्स',
      about: 'ऐप के बारे में',
      logout: 'लॉग आउट'
    },
    history: {
      title: 'कॉल इतिहास',
      all: 'सभी', safe: 'सुरक्षित', suspicious: 'संदिग्ध', scam: 'धोखाधड़ी'
    }
  }
}

const savedLocale = localStorage.getItem('digitalBodyguard.locale') || 'en'
export const locale = ref(savedLocale)

export function setLocale(code) {
  locale.value = code
  localStorage.setItem('digitalBodyguard.locale', code)
}

export function t(key) {
  const dict = dictionaries[locale.value] || dictionaries.en
  const value = key.split('.').reduce((obj, k) => (obj && obj[k] !== undefined ? obj[k] : null), dict)
  return value ?? key
}