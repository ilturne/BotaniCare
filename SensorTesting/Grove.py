import spidev
import time

V_REF = 3.3
ADC_MAX = 4095

DRY_VOLTAGE = 1.0
WET_VOLTAGE = 2.0

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
	if channel not in [0, 1]:
		return -1
	cmd = [1, (2 + channel) << 6, 0]
	reply = spi.xfer2(cmd)
	adc_value = ((reply[1] & 0x0F) << 8) + reply[2]
	return adc_value

def adc_to_voltage(adc_value):
	return (adc_value / ADC_MAX) * V_REF

def voltage_to_moisture(voltage):
	moisture_percentage = ((voltage - DRY_VOLTAGE) / (WET_VOLTAGE - DRY_VOLTAGE)) * 100
	return max(0, min(moisture_percentage, 100))