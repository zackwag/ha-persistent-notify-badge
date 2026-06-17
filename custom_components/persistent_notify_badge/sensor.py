from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SIGNAL_COUNT_CHANGED
from .storage import NotificationStore


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    store: NotificationStore = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NotificationCountSensor(entry, store)])


class NotificationCountSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Unread Count"
    _attr_icon = "mdi:bell-badge"
    _attr_native_unit_of_measurement = "notifications"

    def __init__(self, entry: ConfigEntry, store: NotificationStore) -> None:
        self._store = store
        self._attr_unique_id = f"{entry.entry_id}_unread_count"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Persistent Notify Badge",
            "manufacturer": "zackwag",
        }

    @property
    def native_value(self) -> int:
        return self._store.count()

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_COUNT_CHANGED, self._handle_count_changed
            )
        )

    @callback
    def _handle_count_changed(self) -> None:
        self.async_write_ha_state()
