import lgpio
import time

# FAN_RELAY_PIN = 27

# h = lgpio.gpiochip_open(0)
# lgpio.gpio_claim_output(h, FAN_RELAY_PIN)

def toggle_fan(h, FAN_RELAY_PIN, state: bool):
    lgpio.gpio_write(h, FAN_RELAY_PIN, 1 if state else 0)
    print("Fan turned", "ON" if state else "OFF")

# if __name__ == "__main__":
#     toggle_fan(h, FAN_RELAY_PIN, True)
#     time.sleep(3)
#     toggle_fan(h, FAN_RELAY_PIN, False)
#     lgpio.gpiochip_close(h)
