# Contributing to ha-persistent-notify-badge

A HACS-compatible Home Assistant custom integration that persists
`persistent_notification` entries across restarts and sends iOS badge counts
to mobile app targets. Contributions — bug fixes, new notify target
behaviors, HA compatibility fixes — are welcome.

## Getting started

```
git clone https://github.com/zackwag/ha-persistent-notify-badge.git
cd ha-persistent-notify-badge
pip install pytest pytest-asyncio homeassistant
```

## Development

The integration lives in `custom_components/persistent_notify_badge/`. To
try it in a real Home Assistant instance, copy that directory into your HA
config's `custom_components/` folder and restart HA.

Run the test suite:

```
pytest
```

## Commit messages and pull requests

This repo uses [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `chore:`, etc.). Pull requests are squash-merged, and the **PR title** becomes the commit on `main` — so PR titles must follow this format. This is enforced automatically by the "Conventional Commits" check.

Direct pushes to `main` are allowed but must also use a Conventional Commits-formatted commit message (validated by the same check).

## Opening a pull request

1. Fork the repo and create a branch off `main`.
2. Make your changes.
3. Open a pull request with a Conventional Commits-formatted title.
4. Wait for CI to pass — required checks must be green before merge.

## Reporting issues

Use [GitHub Issues](../../issues) for bugs and feature requests.
