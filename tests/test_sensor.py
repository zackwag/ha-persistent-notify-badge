"""Tests for the notification count sensor entity."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.persistent_notify_badge.sensor import NotificationCountSensor
from custom_components.persistent_notify_badge.storage import NotificationStore


def _make_sensor():
    entry = MagicMock()
    entry.entry_id = "test_entry"

    store = MagicMock(spec=NotificationStore)
    store.count = MagicMock(return_value=0)

    sensor = NotificationCountSensor(entry, store)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()
    return sensor, store


class TestNotificationCountSensor:
    def test_initial_value_zero(self):
        sensor, store = _make_sensor()
        store.count.return_value = 0
        assert sensor.native_value == 0

    def test_value_reflects_store_count(self):
        sensor, store = _make_sensor()
        store.count.return_value = 7
        assert sensor.native_value == 7

    def test_unique_id(self):
        sensor, _ = _make_sensor()
        assert sensor._attr_unique_id == "test_entry_unread_count"

    def test_icon(self):
        sensor, _ = _make_sensor()
        assert sensor._attr_icon == "mdi:bell-badge"

    def test_unit_of_measurement(self):
        sensor, _ = _make_sensor()
        assert sensor._attr_native_unit_of_measurement == "notifications"

    def test_handle_count_changed_writes_state(self):
        sensor, _ = _make_sensor()
        sensor._handle_count_changed()
        sensor.async_write_ha_state.assert_called_once()
