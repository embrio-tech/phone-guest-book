import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin you want to read
PIN = 4  # Change this to the GPIO pin number you're using
DEBOUNCE_TIME = 200  # Debounce time in milliseconds

# Set up the pin as an input
GPIO.setup(PIN, GPIO.IN)

def state_change_callback(channel):
    state = GPIO.input(channel)
    print(f"GPIO {channel} state changed to: {'HIGH' if state else 'LOW'}")

try:
    print(f"Monitoring GPIO pin {PIN}. Press CTRL+C to exit.")
    # Set up event detection for both rising and falling edges
    GPIO.add_event_detect(PIN, GPIO.BOTH, callback=state_change_callback, bouncetime=DEBOUNCE_TIME)
    
    # Keep the script running
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
except RuntimeError as e:
    print(f"Error: {e}")
    print("Try using a different GPIO pin or check if the pin is already in use.")
finally:
    # Clean up GPIO on exit
    GPIO.cleanup()

