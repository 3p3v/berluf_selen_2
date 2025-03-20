"""Berluf Selen 500 integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from berluf_selen_2_ctrl.modbus_impl.pymodbus.serial import Pymodbus_serial_intf_factory
from berluf_selen_2_ctrl.modbus_slave.intf import Device_buildable_intf
from berluf_selen_2_ctrl.recup.device import Recup_device
from berluf_selen_2_ctrl.recup.funcs import (
    Fan_conv,
    Fan_linear_conv,
    Fan_non_conv,
    Recup_persistant,
)
from berluf_selen_2_ctrl.recup.serial import Recup_serial_intf
from homeassistant.const import CONF_PORT, Platform
from homeassistant.helpers.storage import Store

if TYPE_CHECKING:
    from .data import SelenConfigEntry
from .config_flow import CONV_TYPE, INTF_TYPE, ConvType, IntfType
from .const import LOGGER, get_default_store_name
from .data import SelenData
from .persistant import HassModbusPersistant, HassRecupPersistant

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
    Platform.SENSOR,
    Platform.NUMBER,
    Platform.SELECT,
]


def _get_buildable_intf(entry: SelenConfigEntry) -> Device_buildable_intf:
    match entry.data[INTF_TYPE]:
        case IntfType.SERIAL.name:
            return Recup_serial_intf(
                entry.data[CONF_PORT],
                Pymodbus_serial_intf_factory(),
            )

    raise RuntimeError(f"Unknown interface: {entry.data[INTF_TYPE]}.")


def _get_conv(entry: SelenConfigEntry) -> Fan_conv:
    match entry.data[CONV_TYPE]:
        case ConvType.OFF.name:
            return Fan_non_conv()
        case ConvType.LINEAR.name:
            return Fan_linear_conv()

    raise RuntimeError("Unknown conversion.")


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SelenConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    # Interface for connecting to serial
    intf = _get_buildable_intf(entry)
    # Persistant memory
    store = Store[dict[str, dict[int, list[int]]]](
        hass, 1, get_default_store_name(entry.entry_id)
    )
    modbus_persistant = HassModbusPersistant("holding_registers", store)
    # Device
    try:
        mem = await modbus_persistant.load()
        LOGGER.debug(f"Default memory: {mem}")
    except RuntimeError as ec:
        # No saved data found
        LOGGER.info(ec)
        mem = None

    device = Recup_device(intf, mem)

    # Create persistant saver and link it
    persistant = HassRecupPersistant(modbus_persistant)
    Recup_persistant(device, persistant)

    # Save runtime data
    entry.runtime_data = SelenData(intf=intf, device=device, fan_conv=_get_conv(entry))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    LOGGER.debug("Config successfull.")
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: SelenConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: SelenConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
