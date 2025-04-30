import lgpio
import time

# LIGHT_RELAY_PIN = 17

# h = lgpio.gpiochip_open(0)
# lgpio.gpio_claim_output(h, LIGHT_RELAY_PIN)

def toggle_light(h, LIGHT_RELAY_PIN, state: bool):
    lgpio.gpio_write(h, LIGHT_RELAY_PIN, 1 if state else 0)
    print("Light turned", "ON" if state else "OFF")

# if __name__ == "__main__":
#     toggle_light(True)
#     time.sleep(5)
#     toggle_light(False)
#     lgpio.gpiochip_close(h)
