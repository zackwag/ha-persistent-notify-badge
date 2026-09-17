"""Tests for NotificationStore."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.persistent_notify_badge.storage import NotificationStore


def _make_store():
    hass = MagicMock()
    store = NotificationStore(hass)
    store._store = MagicMock()
    store._store.async_load = AsyncMock(return_value=None)
    store._store.async_save = AsyncMock()
    return store


class TestNotificationStore:
    @pytest.mark.asyncio
    async def test_load_empty(self):
        store = _make_store()
        await store.async_load()
        assert store.get_all() == {}
        assert store.count() == 0

    @pytest.mark.asyncio
    async def test_load_existing_data(self):
        store = _make_store()
        store._store.async_load = AsyncMock(
            return_value={"notifications": {"n1": {"title": "Test"}}}
        )
        await store.async_load()
        assert store.count() == 1
        assert store.get_all()["n1"]["title"] == "Test"

    @pytest.mark.asyncio
    async def test_add_and_count(self):
        store = _make_store()
        await store.async_load()

        await store.async_add("n1", {"title": "First"})
        assert store.count() == 1
        store._store.async_save.assert_called()

        await store.async_add("n2", {"title": "Second"})
        assert store.count() == 2

    @pytest.mark.asyncio
    async def test_remove_existing(self):
        store = _make_store()
        await store.async_load()

        await store.async_add("n1", {"title": "First"})
        result = await store.async_remove("n1")
        assert result is True
        assert store.count() == 0

    @pytest.mark.asyncio
    async def test_remove_nonexistent(self):
        store = _make_store()
        await store.async_load()

        result = await store.async_remove("missing")
        assert result is False

    @pytest.mark.asyncio
    async def test_get_all_returns_copy_of_keys(self):
        store = _make_store()
        await store.async_load()
        await store.async_add("n1", {"title": "Test"})

        all_notifs = store.get_all()
        all_notifs.pop("n1")
        assert "n1" in store.get_all()

    @pytest.mark.asyncio
    async def test_save_called_on_add(self):
        store = _make_store()
        await store.async_load()
        store._store.async_save.reset_mock()

        await store.async_add("n1", {"title": "Test"})
        store._store.async_save.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_called_on_remove(self):
        store = _make_store()
        await store.async_load()
        await store.async_add("n1", {"title": "Test"})
        store._store.async_save.reset_mock()

        await store.async_remove("n1")
        store._store.async_save.assert_called_once()
