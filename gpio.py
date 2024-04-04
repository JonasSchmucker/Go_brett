import RPi.GPIO as GPIO
import time

def gpio_init_mode() -> None:
    # Set the pin numbering mode
    GPIO.setmode(GPIO.BCM)

def set_pin_as_output(pin_number: int) -> None:

    GPIO.setup(pin_number, GPIO.OUT)

def set_pin_as_input(pin_number: int) -> None:

    GPIO.setup(pin_number, GPIO.IN)

def set_pin_high(pin_number: int) -> None:

    GPIO.output(pin_number, GPIO.HIGH)

def set_pin_low(pin_number: int) -> None:

    GPIO.output(pin_number, GPIO.LOW)

def gpio_deinit() -> None:
    GPIO.cleanup()

def read_pin(pin_number: int) -> bool:

    input_state = GPIO.input(pin_number)
    
    if input_state == GPIO.HIGH:
        return True
    else:
        return False