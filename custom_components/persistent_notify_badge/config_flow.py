from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import CONF_NOTIFY_TARGETS, DOMAIN


def _targets_schema(defaults: list[str] | None = None) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(
                CONF_NOTIFY_TARGETS,
                default=", ".join(defaults) if defaults else "",
            ): str,
        }
    )


def _parse_targets(raw: str) -> list[str]:
    return [t.strip() for t in raw.split(",") if t.strip()]


class PersistentNotifyBadgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            targets = _parse_targets(user_input[CONF_NOTIFY_TARGETS])
            if not targets:
                errors[CONF_NOTIFY_TARGETS] = "no_targets"
            else:
                return self.async_create_entry(
                    title="Persistent Notify Badge",
                    data={CONF_NOTIFY_TARGETS: targets},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=_targets_schema(),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return PersistentNotifyBadgeOptionsFlow(config_entry)


class PersistentNotifyBadgeOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        current_targets: list[str] = self._config_entry.options.get(
            CONF_NOTIFY_TARGETS,
            self._config_entry.data.get(CONF_NOTIFY_TARGETS, []),
        )

        if user_input is not None:
            targets = _parse_targets(user_input[CONF_NOTIFY_TARGETS])
            if not targets:
                errors[CONF_NOTIFY_TARGETS] = "no_targets"
            else:
                return self.async_create_entry(
                    title="",
                    data={CONF_NOTIFY_TARGETS: targets},
                )

        return self.async_show_form(
            step_id="init",
            data_schema=_targets_schema(current_targets),
            errors=errors,
        )
