from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


async def async_send_badge(hass: HomeAssistant, targets: list[str], count: int) -> None:
    for target in targets:
        service = target if "." in target else f"notify.{target}"
        domain, service_name = service.split(".", 1)
        try:
            await hass.services.async_call(
                domain,
                service_name,
                {
                    "message": "",
                    "data": {
                        "push": {
                            "badge": count,
                        }
                    },
                },
                blocking=False,
            )
        except Exception:
            _LOGGER.exception("Failed to send badge to %s", target)
