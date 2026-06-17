from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import STORAGE_KEY, STORAGE_VERSION


class NotificationStore:
    def __init__(self, hass: HomeAssistant) -> None:
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._notifications: dict[str, dict] = {}

    async def async_load(self) -> None:
        data = await self._store.async_load()
        if data and "notifications" in data:
            self._notifications = data["notifications"]
        else:
            self._notifications = {}

    async def async_save(self) -> None:
        await self._store.async_save({"notifications": self._notifications})

    def get_all(self) -> dict[str, dict]:
        return dict(self._notifications)

    def count(self) -> int:
        return len(self._notifications)

    async def async_add(self, notification_id: str, entry: dict) -> None:
        self._notifications[notification_id] = entry
        await self.async_save()

    async def async_remove(self, notification_id: str) -> bool:
        if notification_id in self._notifications:
            del self._notifications[notification_id]
            await self.async_save()
            return True
        return False
