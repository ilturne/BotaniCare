import spidev
import time

V_REF = 3.3
ADC_MAX = 4095

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

def voltage_to_light_intensity(voltage):
	Dark_Voltage = 0.3
	Bright_Voltage = 2.0
	light_percentage = ((voltage - Dark_Voltage) / (Bright_Voltage - Dark_Voltage)) * 100
	return max(0, min(light_percentage, 100))
