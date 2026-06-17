from __future__ import annotations

import logging
from datetime import datetime, timezone

from homeassistant.components.persistent_notification import (
    UpdateType,
    async_get as pn_async_get,
    async_register_callback,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from .badge import async_send_badge
from .const import (
    ATTR_CREATED_AT,
    ATTR_MESSAGE,
    ATTR_NOTIFICATION_ID,
    ATTR_TITLE,
    CONF_NOTIFY_TARGETS,
    DOMAIN,
)
from .storage import NotificationStore

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    store = NotificationStore(hass)
    await store.async_load()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = store

    # Restore persisted notifications into persistent_notification on reboot
    for notif_id, notif in store.get_all().items():
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "notification_id": notif_id,
                "title": notif.get(ATTR_TITLE, ""),
                "message": notif.get(ATTR_MESSAGE, ""),
            },
            blocking=False,
        )

    # Send initial badge count
    targets = _get_targets(entry)
    await async_send_badge(hass, targets, store.count())

    @callback
    def _handle_notifications_updated(
        update_type: UpdateType, notifications: dict
    ) -> None:
        hass.async_create_task(_async_sync_notifications(hass, entry, store))

    entry.async_on_unload(
        async_register_callback(hass, _handle_notifications_updated)
    )

    entry.async_on_unload(entry.add_update_listener(_async_options_updated))

    return True


async def _async_sync_notifications(
    hass: HomeAssistant, entry: ConfigEntry, store: NotificationStore
) -> None:
    current: dict = pn_async_get(hass)
    stored = store.get_all()

    # Add notifications not yet in storage
    for notif_id, notif in current.items():
        if notif_id not in stored:
            await store.async_add(
                notif_id,
                {
                    ATTR_NOTIFICATION_ID: notif_id,
                    ATTR_TITLE: notif.get("title", ""),
                    ATTR_MESSAGE: notif.get("message", ""),
                    ATTR_CREATED_AT: datetime.now(timezone.utc).isoformat(),
                },
            )

    # Remove notifications that were dismissed
    for notif_id in list(stored.keys()):
        if notif_id not in current:
            await store.async_remove(notif_id)

    # Badge update
    targets = _get_targets(entry)
    await async_send_badge(hass, targets, store.count())


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True


def _get_targets(entry: ConfigEntry) -> list[str]:
    return entry.options.get(
        CONF_NOTIFY_TARGETS,
        entry.data.get(CONF_NOTIFY_TARGETS, []),
    )
