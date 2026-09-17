# AGENTS.md

## Project overview

A HACS-compatible Home Assistant custom integration (Python) that persists
`persistent_notification` entries to HA storage, restores them on reboot,
syncs dismissals, and pushes iOS badge counts via `notify.mobile_app_*`
targets.

## Setup

```
pip install pytest pytest-asyncio homeassistant
```

## Build / Run

N/A — this is a Home Assistant custom component, not a standalone
executable. To exercise it manually, copy
`custom_components/persistent_notify_badge/` into an HA instance's
`custom_components/` directory and restart HA.

## Test

```
pytest
```

Config in `pytest.ini` sets `testpaths = tests` and `asyncio_mode = auto`.
CI (`.github/workflows/test.yml`, `tests.yml`) runs this against Python
3.12/3.13 with `homeassistant` installed as a dependency.

## Repository structure

- `custom_components/persistent_notify_badge/` — the integration:
  `__init__.py` (setup), `config_flow.py` (UI config flow), `storage.py`
  (persistence), `badge.py` (badge count logic), `sensor.py`, `const.py`
- `tests/` — pytest test suite
- `hacs.json` — HACS metadata

## Commit and PR conventions

- Commit messages and PR titles must follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `ci:`, `build:`, `perf:`, `style:`, `revert:`), optionally with a scope, e.g. `fix(api): handle null response`.
- This repo squash-merges pull requests only; the PR title becomes the final commit message on `main`.
- A "Conventional Commits" CI check enforces this on both PR titles and direct-push commit messages.
- Branch protection on `main`: no force-pushes, no branch deletion, required status checks must pass.
