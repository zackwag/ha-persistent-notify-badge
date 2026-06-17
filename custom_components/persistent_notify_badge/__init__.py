from __future__ import annotations

import logging
from datetime import datetime, timezone

from homeassistant.components.persistent_notification import (
    UpdateType,
    async_create as pn_async_create,
    async_register_callback,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .badge import async_send_badge
from .const import (
    ATTR_CREATED_AT,
    ATTR_MESSAGE,
    ATTR_NOTIFICATION_ID,
    ATTR_TITLE,
    CONF_NOTIFY_TARGETS,
    DOMAIN,
    SIGNAL_COUNT_CHANGED,
)
from .storage import NotificationStore

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    store = NotificationStore(hass)
    await store.async_load()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = store

    @callback
    def _handle_notifications_updated(
        update_type: UpdateType, notifications: dict
    ) -> None:
        hass.async_create_task(
            _async_handle_update(hass, entry, store, update_type, notifications)
        )

    entry.async_on_unload(
        async_register_callback(hass, _handle_notifications_updated)
    )

    # Restore persisted notifications — triggers ADDED callbacks which are
    # no-ops for already-stored IDs, so storage stays consistent
    for notif_id, notif in store.get_all().items():
        pn_async_create(
            hass,
            notif.get(ATTR_MESSAGE, ""),
            notif.get(ATTR_TITLE) or None,
            notif_id,
        )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Send initial badge with count from storage
    await async_send_badge(hass, _get_targets(entry), store.count())

    entry.async_on_unload(entry.add_update_listener(_async_options_updated))
    return True


async def _async_handle_update(
    hass: HomeAssistant,
    entry: ConfigEntry,
    store: NotificationStore,
    update_type: UpdateType,
    notifications: dict,
) -> None:
    changed = False
    stored = store.get_all()

    if update_type == UpdateType.ADDED:
        for notif_id, notif in notifications.items():
            if notif_id not in stored:
                created_at = notif.get("created_at")
                await store.async_add(
                    notif_id,
                    {
                        ATTR_NOTIFICATION_ID: notif_id,
                        ATTR_TITLE: notif.get("title", ""),
                        ATTR_MESSAGE: notif.get("message", ""),
                        ATTR_CREATED_AT: (
                            created_at.isoformat()
                            if hasattr(created_at, "isoformat")
                            else datetime.now(timezone.utc).isoformat()
                        ),
                    },
                )
                changed = True

    elif update_type == UpdateType.REMOVED:
        for notif_id in notifications:
            if await store.async_remove(notif_id):
                changed = True

    if changed:
        async_dispatcher_send(hass, SIGNAL_COUNT_CHANGED)
        await async_send_badge(hass, _get_targets(entry), store.count())


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True


def _get_targets(entry: ConfigEntry) -> list[str]:
    return entry.options.get(
        CONF_NOTIFY_TARGETS,
        entry.data.get(CONF_NOTIFY_TARGETS, []),
    )
