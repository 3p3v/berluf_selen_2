from typing import Tuple
from .memory import Memory_rw


# %%
class Slave_builder:
    """Base class for creating and adding slaves to the interface"""

    # TODO create method to generate memory
    # TODO create method 'attach' to attach device to intf

    def create_slave(self) -> Tuple[Memory_rw, Memory_rw, Memory_rw, Memory_rw]:
        raise NotImplementedError()


# %%
class Device_intf:
    """Base for modbus device connectivity interface"""

    async def connect(self) -> None:
        raise NotImplementedError()

    async def disconnect(self) -> None:
        raise NotImplementedError()


class Device_buildable_intf(Slave_builder, Device_intf):
    def __init__(self):
        return
