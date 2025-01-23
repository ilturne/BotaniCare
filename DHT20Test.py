import time
from smbus2 import SMBus

# I2C address of the DHT20 sensor
DHT20_ADDRESS = 0x38

# Function to initialize the DHT20 sensor
def initialize_dht20(bus):
    bus.write_byte(DHT20_ADDRESS, 0xAC)  # Initialize measurement
    time.sleep(0.1)

# Function to read data from the DHT20 sensor
def read_dht20(bus):
    # Send measurement request
    bus.write_byte(DHT20_ADDRESS, 0xAC)
    time.sleep(0.1)

    # Read 7 bytes of data
    data = bus.read_i2c_block_data(DHT20_ADDRESS, 0x00, 7)

    # Parse the temperature and humidity
    if (data[0] & 0x80) == 0:  # Check if data is valid
        humidity_raw = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4)) & 0xFFFFF
        temperature_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

        # Convert raw data to actual values
        humidity = (humidity_raw / 0x100000) * 100
        temperature = ((temperature_raw / 0x100000) * 200) - 50

        return temperature, humidity
    else:
        raise ValueError("Invalid data from DHT20 sensor")

# Main program
def main():
    try:
        # Initialize I2C bus
        bus = SMBus(1)

        # Initialize the sensor
        initialize_dht20(bus)

        while True:
            try:
                # Read temperature and humidity
                temperature, humidity = read_dht20(bus)

                # Print results
                print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%")

                # Wait before the next reading
                time.sleep(2)
            except ValueError as e:
                print(f"Error: {e}")
                time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
