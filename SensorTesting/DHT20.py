import time
from smbus2 import SMBus

class DFRobot_DHT20:
    def __init__(self, bus: int, address: int) -> None:
        self.i2cbus = SMBus(bus)
        self._addr = address

    def begin(self) -> bool:
        time.sleep(0.5)
        data = self.__read_reg(0x71, 1)
        return (data[0] & 0x18) == 0x18

    def get_temperature_and_humidity(self):
        self.__write_reg(0xAC, [0x33, 0x00])
        while True:
            time.sleep(0.08)
            data = self.__read_reg(0x71, 1)
            if (data[0] & 0x80) == 0:
                break

        data = self.__read_reg(0x71, 7)
        hum_raw = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4))
        temp_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        humidity = (hum_raw / 0x100000) * 100
        temperature = (temp_raw / 5242.88) - 50

        # CRC Validation
        crc_error = self.__calc_crc8(data) != data[6]

        return temperature, humidity, crc_error

    def __calc_crc8(self, data):
        crc = 0xFF
        for byte in data[:-1]:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc <<= 1
            crc &= 0xFF
        return crc

    def __write_reg(self, reg: int, data: list[int]) -> None:
        time.sleep(0.01)
        self.i2cbus.write_i2c_block_data(self._addr, reg, data)

    def __read_reg(self, reg: int, length: int) -> list[int]:
        time.sleep(0.01)
        return self.i2cbus.read_i2c_block_data(self._addr, reg, length)


# Main script
if __name__ == "__main__":
    DHT20_I2C_BUS = 1
    DHT20_I2C_ADDR = 0x38

    dht20 = DFRobot_DHT20(DHT20_I2C_BUS, DHT20_I2C_ADDR)

    if not dht20.begin():
        print("Failed to initialize DHT20 sensor.")
    else:
        print("DHT20 initialized successfully.")
        try:
            while True:
                temp, hum, crc_error = dht20.get_temperature_and_humidity()
                if crc_error:
                    print("CRC check failed! Data may be invalid.")
                else:
                    print(f"Temperature: {temp:.2f} °C, Humidity: {hum:.2f} %")
                time.sleep(2)
        except KeyboardInterrupt:
            print("Exiting program.")
