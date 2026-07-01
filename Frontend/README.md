# Digital Bodyguard — Vue Frontend

All 20 screens are already built and wired together with Vue Router, so you can run
the whole flow today. The day-by-day list below is just a suggested order if you (or
your team) want to review, present, or extend the screens gradually — 2 per day, 10 days.

## Run it

```bash
npm install
npm run dev
```

Then open the local URL Vite prints (usually http://localhost:5173).
It starts on the Splash screen and auto-navigates to Onboarding.

## Suggested demo flow

Onboarding → Register/Login → Dashboard → tap "Emergency" or open Incoming Call route
manually (`/incoming-call`) → Accept → Voice Analysis (auto-analyzes for ~2s) →
Scam Result → Call Family → Family Alert confirmation.

## Build schedule (2 screens/day)

| Day | Screens |
|---|---|
| 1 | Splash Screen, Welcome/Onboarding |
| 2 | Login, Register |
| 3 | Home Dashboard, Incoming Call |
| 4 | Voice Analysis, Safe Call Result |
| 5 | Suspicious Call Result, Scam Detected |
| 6 | Family Alert, Call History |
| 7 | Call Details, Notifications |
| 8 | Emergency Contacts, Settings |
| 9 | Profile, Help & Support |
| 10 | About, Logout Confirmation |

## File map

- `src/router/index.js` — all routes/paths for the 20 screens
- `src/views/*.vue` — one file per screen (see comment at top of each file for its "day")
- `src/components/AppShell.vue` — shared bottom nav bar used on Dashboard/History/Notifications/Contacts/Profile
- `src/assets/theme.css` — shared design tokens (colors, buttons, cards) — edit here to reskin the whole app at once

## Where your teammate's work plugs in

- `SettingsView.vue` → Privacy Settings row → link to their encryption/data controls
- `VoiceAnalysisView.vue` → replace the fake progress timer with their real detection API call
- `FamilyAlertView.vue` → replace the static "Delivered" state with their real SMS/push send result
- `LoginView.vue` / `RegisterView.vue` → connect to their auth/backend endpoints
