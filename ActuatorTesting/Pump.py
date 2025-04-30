import lgpio
import time

# PUMP_CTRL_PIN = 22

# h = lgpio.gpiochip_open(0)
# lgpio.gpio_claim_output(h, PUMP_CTRL_PIN)

def toggle_pump(h, PUMP_CTRL_PIN, state: bool):
    lgpio.gpio_write(h, PUMP_CTRL_PIN, 1 if state else 0)
    print("Pump turned", "ON" if state else "OFF")

# if __name__ == "__main__":
#     toggle_pump(True)
#     time.sleep(1)
#     toggle_pump(False)
#     lgpio.gpiochip_close(h)
