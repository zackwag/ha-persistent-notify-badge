# Persistent Notify Badge

A HACS-compatible Home Assistant custom integration that:

- **Persists** all `persistent_notification` entries to HA's storage layer
- **Restores** them on reboot (so notifications survive HA restarts)
- **Dismissal syncing** — when a notification is dismissed in the UI, it is removed from storage
- **Badge counts** — sends an iOS badge count to one or more `notify.mobile_app_*` targets whenever the notification count changes

## Installation

### HACS (recommended)

1. In HACS → Integrations → ⋮ → Custom repositories
2. Add `https://github.com/zackwag/ha-persistent-notify-badge` as an **Integration**
3. Install **Persistent Notify Badge**
4. Restart Home Assistant

### Manual

Copy `custom_components/persistent_notify_badge/` into your `config/custom_components/` directory and restart.

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Persistent Notify Badge**
3. Enter your notify target(s), comma-separated — e.g. `notify.mobile_app_my_iphone`

You can update targets at any time via the integration's **Configure** button.

## How it works

| Event | Action |
|---|---|
| New `persistent_notification` created | Saved to storage; badge count incremented |
| Notification dismissed in UI | Removed from storage; badge count decremented |
| HA restarts | All stored notifications recreated; badge sent with current count |
| Notify targets changed | Integration reloads and resumes with new targets |

## iOS badge notes

Badge updates are sent as silent push notifications (`message: ""`). iOS will not display an alert — only the app icon badge number changes. Make sure the Home Assistant Companion App has notification permissions on the device.

Android badge support varies by launcher and is not officially guaranteed, but the same `push.badge` field is sent so compatible launchers may display a count.
