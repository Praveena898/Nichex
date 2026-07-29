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
  },
  kok: {
    nav: { home: 'घर', history: 'इतिहास', alerts: 'सतर्कता', contacts: 'कुटुंब', profile: 'प्रोफायल' },
    common: { applyChanges: 'बदल लागू करात', applied: 'लागू जाला ✓', cancel: 'रद्द करात', continueText: 'फुडें वचात' },
    splash: { name: 'डिजिटल बॉडीगार्ड', tagline: 'दर एका कॉलाची सुरक्षा, दर दिस' },
    onboarding: { getStarted: 'सुरू करात', haveAccount: 'म्हज्याकडे पयलीच खातें आसा', next: 'फुडें' },
    login: {
      title: 'परत येवकार',
      subtitle: 'सुरक्षा चालू दवरपाक लॉगीन करात',
      emailLabel: 'ईमेल वा फोन',
      passwordLabel: 'पासवर्ड',
      remember: 'म्हाका याद दवरात',
      forgot: 'पासवर्ड विसरलात?',
      button: 'लॉगीन करात',
      noAccount: 'नवे आसात?',
      createAccount: 'खातें तयार करात'
    },
    register: {
      title: 'खातें तयार करात',
      nameLabel: 'पुराय नांव',
      phoneLabel: 'फोन नंबर',
      emailLabel: 'ईमेल',
      passwordLabel: 'पासवर्ड',
      contactLabel: 'आणीबाणीचो संपर्क (कुटुंब)',
      button: 'खातें तयार करात',
      haveAccount: 'पयलीच खातें आसा?',
      login: 'लॉगीन करात'
    },
    dashboard: {
      greeting: 'दनपारां बरे,',
      status: 'सुरक्षा स्थिती',
      active: 'सक्रीय आनी देखरेख करता',
      today: 'आयचें काम',
      calls: 'कॉल्स', safe: 'सुरक्षीत', suspicious: 'संशयास्पद', scam: 'फसवणूक',
      recent: 'अलीकडले कॉल्स',
      quickActions: 'त्वरीत कारवाय',
      callHistory: 'कॉल इतिहास',
      contacts: 'संपर्क',
      emergency: 'आणीबाणी — कुटुंबाक कळयात'
    },
    settings: {
      title: 'सेटिंग्स',
      darkMode: 'डार्क मोड',
      language: 'भाशा',
      accessibility: 'प्रवेशयोग्यताय (व्हड मजकूर)',
      notifications: 'सुचोवणी सेटिंग्स',
      privacy: 'खाजगीपण सेटिंग्स',
      about: 'ह्या ऍपाविशीं',
      logout: 'लॉगआवुट'
    },
    history: {
      title: 'कॉल इतिहास',
      all: 'सगळें', safe: 'सुरक्षीत', suspicious: 'संशयास्पद', scam: 'फसवणूक'
    }
  },
  ml: {
    nav: { home: 'ഹോം', history: 'ചരിത്രം', alerts: 'അലേർട്ടുകൾ', contacts: 'കുടുംബം', profile: 'പ്രൊഫൈൽ' },
    common: { applyChanges: 'മാറ്റങ്ങൾ പ്രയോഗിക്കുക', applied: 'പ്രയോഗിച്ചു ✓', cancel: 'റദ്ദാക്കുക', continueText: 'തുടരുക' },
    splash: { name: 'ഡിജിറ്റൽ ബോഡിഗാർഡ്', tagline: 'ഓരോ കോളും, ഓരോ ദിവസവും സംരക്ഷിക്കുന്നു' },
    onboarding: { getStarted: 'ആരംഭിക്കുക', haveAccount: 'എനിക്ക് ഇതിനകം ഒരു അക്കൗണ്ട് ഉണ്ട്', next: 'അടുത്തത്' },
    login: {
      title: 'തിരികെ സ്വാഗതം',
      subtitle: 'സംരക്ഷണം സജീവമായി നിലനിർത്താൻ ലോഗിൻ ചെയ്യുക',
      emailLabel: 'ഇമെയിൽ അല്ലെങ്കിൽ ഫോൺ',
      passwordLabel: 'പാസ്‌വേഡ്',
      remember: 'എന്നെ ഓർക്കുക',
      forgot: 'പാസ്‌വേഡ് മറന്നോ?',
      button: 'ലോഗിൻ ചെയ്യുക',
      noAccount: 'പുതിയതാണോ?',
      createAccount: 'ഒരു അക്കൗണ്ട് സൃഷ്ടിക്കുക'
    },
    register: {
      title: 'അക്കൗണ്ട് സൃഷ്ടിക്കുക',
      nameLabel: 'മുഴുവൻ പേര്',
      phoneLabel: 'ഫോൺ നമ്പർ',
      emailLabel: 'ഇമെയിൽ',
      passwordLabel: 'പാസ്‌വേഡ്',
      contactLabel: 'അടിയന്തര ബന്ധം (കുടുംബം)',
      button: 'അക്കൗണ്ട് സൃഷ്ടിക്കുക',
      haveAccount: 'ഇതിനകം അക്കൗണ്ട് ഉണ്ടോ?',
      login: 'ലോഗിൻ ചെയ്യുക'
    },
    dashboard: {
      greeting: 'ഉച്ചയ്ക്ക് ശേഷം നമസ്കാരം,',
      status: 'സംരക്ഷണ നില',
      active: 'സജീവം & നിരീക്ഷണത്തിൽ',
      today: 'ഇന്നത്തെ പ്രവർത്തനം',
      calls: 'കോളുകൾ', safe: 'സുരക്ഷിതം', suspicious: 'സംശയാസ്‌പദം', scam: 'തട്ടിപ്പ്',
      recent: 'സമീപകാല കോളുകൾ',
      quickActions: 'ദ്രുത പ്രവർത്തനങ്ങൾ',
      callHistory: 'കോൾ ചരിത്രം',
      contacts: 'ബന്ധങ്ങൾ',
      emergency: 'അടിയന്തരാവസ്ഥ — എന്റെ കുടുംബത്തെ അറിയിക്കുക'
    },
    settings: {
      title: 'ക്രമീകരണങ്ങൾ',
      darkMode: 'ഡാർക്ക് മോഡ്',
      language: 'ഭാഷ',
      accessibility: 'ഉപയോഗസൗകര്യം',
      notifications: 'അറിയിപ്പ് ക്രമീകരണങ്ങൾ',
      privacy: 'സ്വകാര്യതാ ക്രമീകരണങ്ങൾ',
      about: 'ഈ ആപ്പിനെക്കുറിച്ച്',
      logout: 'ലോഗ് ഔട്ട്'
    },
    history: {
      title: 'കോൾ ചരിത്രം',
      all: 'എല്ലാം', safe: 'സുരക്ഷിതം', suspicious: 'സംശയാസ്‌പദം', scam: 'തട്ടിപ്പ്'
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