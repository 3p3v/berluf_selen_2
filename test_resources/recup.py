import asyncio

from pymodbus_3p3v.client import ModbusSerialClient as ModbusClient


class Recup:
    def __init__(self, cli: ModbusClient):
        self._addr = 1
        self._cli = cli
        self._01 = 20
        self._02 = 24
        self._03 = 23
        self._04 = 22
        self._05 = 21
        self._ec = 0

    def set_01(self, temp: int):
        self._01 = temp

    def set_02(self, temp: int):
        self._02 = temp

    def set_03(self, temp: int):
        self._03 = temp

    def set_04(self, temp: int):
        self._04 = temp

    def set_05(self, temp: int):
        self._05 = temp

    def set_error(self, ec: str):
        self._ec = int(ec, 2)

    def send_regs(self) -> int:
        self._cli.write_register(258, self._ec, slave=self._addr)
        self._cli.write_register(259, self._01, slave=self._addr)
        self._cli.write_register(260, self._02, slave=self._addr)
        self._cli.write_register(261, self._03, slave=self._addr)
        self._cli.write_register(262, self._04, slave=self._addr)
        self._cli.write_register(263, self._05, slave=self._addr)
        print("WRITE")
        return 0

    def receive_holding_regs(self):  # for now ignore values
        try:
            print(
                f"0:   {self._cli.read_holding_registers(0, 11, slave=self._addr).registers}"
            )
            print(
                f"60:  {self._cli.read_holding_registers(60, 13, slave=self._addr).registers}"
            )
            print(
                f"275: {self._cli.read_holding_registers(274, 5, slave=self._addr).registers}"
            )
        except:
            print("ERROR")


async def main():
    while True:
        cli = ModbusClient(
            port="/srv/pts/ttyV0", baudrate=9600, bytesize=8, parity="N", stopbits=1
        )

        recup = Recup(cli)

        recup.set_error("00000000")
        recup.send_regs()

        recup.receive_holding_regs()

        cli.close()


asyncio.run(main())
