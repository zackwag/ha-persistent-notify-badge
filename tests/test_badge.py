"""Tests for badge sending logic."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.persistent_notify_badge.badge import async_send_badge


class TestAsyncSendBadge:
    @pytest.mark.asyncio
    async def test_sends_badge_to_each_target(self):
        hass = MagicMock()
        hass.services.async_call = AsyncMock()

        await async_send_badge(hass, ["mobile_app_phone", "mobile_app_tablet"], 5)

        assert hass.services.async_call.call_count == 2

        first_call = hass.services.async_call.call_args_list[0]
        assert first_call[0] == (
            "notify",
            "mobile_app_phone",
            {"message": "", "data": {"push": {"badge": 5}}},
        )
        assert first_call[1] == {"blocking": False}

        second_call = hass.services.async_call.call_args_list[1]
        assert second_call[0] == (
            "notify",
            "mobile_app_tablet",
            {"message": "", "data": {"push": {"badge": 5}}},
        )

    @pytest.mark.asyncio
    async def test_handles_dotted_service_name(self):
        hass = MagicMock()
        hass.services.async_call = AsyncMock()

        await async_send_badge(hass, ["notify.my_phone"], 3)

        call = hass.services.async_call.call_args_list[0]
        assert call[0][0] == "notify"
        assert call[0][1] == "my_phone"

    @pytest.mark.asyncio
    async def test_zero_count(self):
        hass = MagicMock()
        hass.services.async_call = AsyncMock()

        await async_send_badge(hass, ["mobile_app_phone"], 0)

        call = hass.services.async_call.call_args_list[0]
        assert call[0][2]["data"]["push"]["badge"] == 0

    @pytest.mark.asyncio
    async def test_empty_targets(self):
        hass = MagicMock()
        hass.services.async_call = AsyncMock()

        await async_send_badge(hass, [], 5)

        hass.services.async_call.assert_not_called()

    @pytest.mark.asyncio
    async def test_service_call_failure_does_not_raise(self):
        hass = MagicMock()
        hass.services.async_call = AsyncMock(side_effect=Exception("service error"))

        await async_send_badge(hass, ["mobile_app_phone"], 1)
