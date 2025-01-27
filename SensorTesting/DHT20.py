import time
from smbus2 import SMBus

class DFRobot_DHT20:
    """Class for interacting with the DHT20 Temperature and Humidity Sensor."""

    def __init__(self, bus: int, address: int) -> None:
        self.i2cbus = SMBus(bus)
        self._addr = address

    def begin(self) -> bool:
        """Initialize the sensor and check readiness."""
        time.sleep(0.5)  # Wait at least 100ms after power-on
        data = self.__read_reg(0x71, 1)
        return (data[0] & 0x18) == 0x18

    def get_temperature_and_humidity(self) -> tuple[float, float, bool]:
        """Read and return temperature, humidity, and CRC status."""
        # Trigger measurement
        self.__write_reg(0xAC, [0x33, 0x00])

        # Wait for the measurement to complete
        while True:
            time.sleep(0.08)
            data = self.__read_reg(0x71, 1)
            if (data[0] & 0x80) == 0:
                break

        # Read sensor data
        data = self.__read_reg(0x71, 7)

        # Extract and calculate temperature and humidity
        temp_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        hum_raw = ((data[3] & 0xF0) >> 4) | (data[1] << 12) | (data[2] << 4)
        temperature = temp_raw / 5242.88 - 50  # Convert to Celsius
        humidity = hum_raw / 0x100000 * 100  # Convert to percentage

        # Check CRC
        crc_error = self.__calc_crc8(data) != data[6]

        return temperature, humidity, crc_error

    def __calc_crc8(self, data: list[int]) -> int:
        """Calculate the CRC-8 checksum."""
        crc = 0xFF
        for byte in data[:-1]:
            crc ^= byte
            for _ in range(8):
                crc = (crc << 1) ^ 0x31 if crc & 0x80 else crc << 1
        return crc & 0xFF

    def __write_reg(self, reg: int, data: list[int]) -> None:
        """Write data to a sensor register."""
        time.sleep(0.01)
        self.i2cbus.write_i2c_block_data(self._addr, reg, data)

    def __read_reg(self, reg: int, length: int) -> list[int]:
        """Read data from a sensor register."""
        time.sleep(0.01)
        return self.i2cbus.read_i2c_block_data(self._addr, reg, length)


# Main script
if __name__ == "__main__":
    DHT20_I2C_BUS = 1  # I2C bus number
    DHT20_I2C_ADDR = 0x38  # DHT20 I2C address

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
                time.sleep(2)  # Wait before the next read
        except KeyboardInterrupt:
            print("Exiting program.")
