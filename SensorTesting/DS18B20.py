import os
import glob
import time

BASE_DIR = "/sys/bus/w1/devices/"
device_folder = glob.glob(BASE_DIR + "28*")[0]
device_file = device_folder + "/w1_slave"

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

def read_temp_raw():
    with open(device_file, "r") as f:
        lines = f.readlines()
    return lines

def read_temp():
    lines = read_temp_raw()
    while "YES" not in lines[0]:
        time.sleep(0.2)
        lines = read_temp_raw()

    temp_output = lines[1].split("t=")[-1]
    temp_celsius = float(temp_output) / 1000.0
    temp_farenheit = (temp_celsius * 9.0 / 5.0) + 32.0

    return temp_celsius, temp_farenheit

try:
    while True:
        temp_c, temp_f = read_temp()
        print(f"Temperature: {temp_c:.2f} C | {temp_f:.2f} F")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting")
