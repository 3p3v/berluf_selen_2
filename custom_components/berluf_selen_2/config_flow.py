"""Config flow for berluf_selen_500."""

from __future__ import annotations

from enum import Enum

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_PORT
from homeassistant.helpers import selector

from .const import DOMAIN, LOGGER

# Conversion
CONV_TYPE = "fans_conv"


class ConvType(Enum):
    """Fan speed conversion options."""

    off = 0
    linear = 1


# Intefrace
INTF_TYPE = "intf_type"


class IntfType(Enum):
    """Types of interfaces (low-level connection with recuperator)."""

    serial = 0


class SelenFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    _data: dict[str, str] = {}

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Set up the fan conversion and interface type."""
        _errors = {}
        if user_input is not None:
            # Check if fan speed conversion was set
            conv_type = user_input.get(CONV_TYPE)
            intf_type = user_input.get(INTF_TYPE)
            if conv_type is not None and intf_type is not None:
                # Update data
                self._data[CONV_TYPE] = conv_type
                self._data[INTF_TYPE] = intf_type

                # Conversion and interface already set, get interface specyfic data
                match user_input[INTF_TYPE]:
                    case IntfType.serial.name:
                        # Specify serial port
                        LOGGER.debug("Serial chosen")
                        return await self.async_step_serial()

                # Interface not recognised
                raise RuntimeError(f"Unknown interface type: {user_input[INTF_TYPE]}.")

        # First select interface type
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONV_TYPE,
                    ): selector.SelectSelector(
                        config=selector.SelectSelectorConfig(
                            options=[ct.name for ct in ConvType]
                        )
                    ),
                    vol.Required(
                        INTF_TYPE,
                    ): selector.SelectSelector(
                        config=selector.SelectSelectorConfig(
                            options=[it.name for it in IntfType]
                        )
                    ),
                },
            ),
            errors=_errors,
        )

    async def async_step_serial(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Set serial port name."""
        LOGGER.debug("Entering serial config")
        _errors = {}
        if user_input is not None:
            conf_port = user_input.get(CONF_PORT)
            if conf_port is not None:
                # All data aquired
                self._data[CONF_PORT] = conf_port
                return self.async_create_entry(
                    title=user_input[CONF_PORT],
                    data=self._data,
                )

        return self.async_show_form(
            step_id="serial",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_PORT,
                        default=(user_input or {}).get(CONF_PORT, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )
