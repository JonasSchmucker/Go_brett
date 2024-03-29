import RPi.GPIO as GPIO
import time

initialized = False

def gpio_init_mode() -> None:
    # Set the pin numbering mode
    GPIO.setmode(GPIO.BCM)

def set_pin_as_output(pin_number: int) -> None:
    if not initialized:
        gpio_init_mode()
        initialized = True
    GPIO.setup(pin_number, GPIO.OUT)

def set_pin_as_input(pin_number: int) -> None:
    if not initialized:
        gpio_init_mode()
        initialized = True
    GPIO.setup(pin_number, GPIO.IN)

def set_pin_high(pin_number: int) -> None:
    if not initialized:
        gpio_init_mode()
        initialized = True
    GPIO.output(pin_number, GPIO.HIGH)

def set_pin_low(pin_number: int) -> None:
    if not initialized:
        gpio_init_mode()
        initialized = True
    GPIO.output(pin_number, GPIO.LOW)

def gpio_deinit() -> None:
    GPIO.cleanup()

def read_pin(pin_number: int) -> bool:
    if not initialized:
        gpio_init_mode()
        initialized = True
    input_state = GPIO.input(pin_number)
    
    if input_state == GPIO.HIGH:
        return True
    else:
        return False