"""Tests for config flow and options flow."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from custom_components.persistent_notify_badge.config_flow import (
    PersistentNotifyBadgeConfigFlow,
    PersistentNotifyBadgeOptionsFlow,
    _parse_targets,
    _targets_schema,
)
from custom_components.persistent_notify_badge.const import CONF_NOTIFY_TARGETS


class TestParseTargets:
    def test_single_target(self):
        assert _parse_targets("mobile_app_phone") == ["mobile_app_phone"]

    def test_multiple_targets(self):
        assert _parse_targets("mobile_app_phone, mobile_app_tablet") == [
            "mobile_app_phone",
            "mobile_app_tablet",
        ]

    def test_strips_whitespace(self):
        assert _parse_targets("  phone , tablet  ") == ["phone", "tablet"]

    def test_empty_string(self):
        assert _parse_targets("") == []

    def test_only_commas(self):
        assert _parse_targets(",,,") == []

    def test_trailing_comma(self):
        assert _parse_targets("phone,") == ["phone"]


class TestUserStep:
    @pytest.mark.asyncio
    async def test_no_input_shows_form(self):
        flow = PersistentNotifyBadgeConfigFlow()
        flow.hass = MagicMock()

        result = await flow.async_step_user(None)

        assert result["type"] == "form"
        assert result["step_id"] == "user"

    @pytest.mark.asyncio
    async def test_valid_targets_creates_entry(self):
        flow = PersistentNotifyBadgeConfigFlow()
        flow.hass = MagicMock()

        result = await flow.async_step_user(
            {CONF_NOTIFY_TARGETS: "mobile_app_phone, mobile_app_tablet"}
        )

        assert result["type"] == "create_entry"
        assert result["title"] == "Persistent Notify Badge"
        assert result["data"][CONF_NOTIFY_TARGETS] == [
            "mobile_app_phone",
            "mobile_app_tablet",
        ]

    @pytest.mark.asyncio
    async def test_empty_targets_shows_error(self):
        flow = PersistentNotifyBadgeConfigFlow()
        flow.hass = MagicMock()

        result = await flow.async_step_user({CONF_NOTIFY_TARGETS: ""})

        assert result["type"] == "form"
        assert result["errors"][CONF_NOTIFY_TARGETS] == "no_targets"


class TestOptionsFlow:
    @pytest.mark.asyncio
    async def test_no_input_shows_form(self):
        entry = MagicMock()
        entry.options = {}
        entry.data = {CONF_NOTIFY_TARGETS: ["mobile_app_phone"]}

        flow = PersistentNotifyBadgeOptionsFlow(entry)

        result = await flow.async_step_init(None)

        assert result["type"] == "form"
        assert result["step_id"] == "init"

    @pytest.mark.asyncio
    async def test_valid_targets_creates_entry(self):
        entry = MagicMock()
        entry.options = {CONF_NOTIFY_TARGETS: ["mobile_app_phone"]}
        entry.data = {}

        flow = PersistentNotifyBadgeOptionsFlow(entry)

        result = await flow.async_step_init(
            {CONF_NOTIFY_TARGETS: "mobile_app_tablet"}
        )

        assert result["type"] == "create_entry"
        assert result["data"][CONF_NOTIFY_TARGETS] == ["mobile_app_tablet"]

    @pytest.mark.asyncio
    async def test_empty_targets_shows_error(self):
        entry = MagicMock()
        entry.options = {}
        entry.data = {CONF_NOTIFY_TARGETS: ["phone"]}

        flow = PersistentNotifyBadgeOptionsFlow(entry)

        result = await flow.async_step_init({CONF_NOTIFY_TARGETS: ""})

        assert result["type"] == "form"
        assert result["errors"][CONF_NOTIFY_TARGETS] == "no_targets"
