import gpio

__GPIO_PIN_MUL_LED_IN_ADDRESS_START__ = 0
__GPIO_PIN_MUL_LED_OUT_ADDRESS_START__ = 0

__GPIO_PIN_EXTRA_LED_IN_1__ = 0
__GPIO_PIN_EXTRA_LED_IN_2__ = 0
__GPIO_PIN_EXTRA_LED_IN_3__ = 0

__GPIO_PIN_EXTRA_LED_OUT_1__ = 0
__GPIO_PIN_EXTRA_LED_OUT_2__ = 0
__GPIO_PIN_EXTRA_LED_OUT_3__ = 0

__GPIO_PIN_MUL_LED_OUT_ENABLE__ = 0
__GPIO_PIN_MUL_LED_IN_ENABLE__ = 0

current_x = -1
current_y = -1

def set_led(x: int, y: int):
    return



def write_address_in(address: int):
    if address >= 16 or address < 0:
        print("Invalid address" + str(address))
        return
    
    if address >= 8:
        address -= 8
        gpio.set_pin_high(__GPIO_PIN_MUL_LED_IN_ADDRESS_START__)
    else:
        gpio.set_pin_low(__GPIO_PIN_MUL_LED_IN_ADDRESS_START__)

    if address >= 4:
        address -= 4
        gpio.set_pin_high(__GPIO_PIN_MUL_LED_IN_ADDRESS_START__ + 1)
    else:
        gpio.set_pin_low(__GPIO_PIN_MUL_LED_IN_ADDRESS_START__ + 1)

    if address >= 2:
        address -= 2
        gpio.set_pin_high(__GPIO_PIN_MUL_LED_IN_ADDRESS_START__ + 2)
    else:
        gpio.set_pin_low(__GPIO_PIN_MUL_LED_IN_ADDRESS_START__ + 2)

    if address >= 1:
        address -= 1
        gpio.set_pin_high(__GPIO_PIN_MUL_LED_IN_ADDRESS_START__ + 3)
    else:
        gpio.set_pin_low(__GPIO_PIN_MUL_LED_IN_ADDRESS_START__ + 3)

def write_address_out(address: int):
    if address >= 16 or address < 0:
        print("Invalid address" + str(address))
        return
    
    if address >= 8:
        address -= 8
        gpio.set_pin_high(__GPIO_PIN_MUL_LED_OUT_ADDRESS_START__)
    else:
        gpio.set_pin_low(__GPIO_PIN_MUL_LED_OUT_ADDRESS_START__)

    if address >= 4:
        address -= 4
        gpio.set_pin_high(__GPIO_PIN_MUL_LED_OUT_ADDRESS_START__ + 1)
    else:
        gpio.set_pin_low(__GPIO_PIN_MUL_LED_OUT_ADDRESS_START__ + 1)

    if address >= 2:
        address -= 2
        gpio.set_pin_high(__GPIO_PIN_MUL_LED_OUT_ADDRESS_START__ + 2)
    else:
        gpio.set_pin_low(__GPIO_PIN_MUL_LED_OUT_ADDRESS_START__ + 2)

    if address >= 1:
        address -= 1
        gpio.set_pin_high(__GPIO_PIN_MUL_LED_OUT_ADDRESS_START__ + 3)
    else:
        gpio.set_pin_low(__GPIO_PIN_MUL_LED_OUT_ADDRESS_START__ + 3)


def init_leds():
    gpio.set_pin_as_output(__GPIO_PIN_MUL_LED_OUT_ENABLE__)
    gpio.set_pin_as_output(__GPIO_PIN_MUL_LED_IN_ENABLE__)
    
    gpio.set_pin_low(__GPIO_PIN_MUL_LED_OUT_ENABLE__)
    gpio.set_pin_low(__GPIO_PIN_MUL_LED_OUT_ENABLE__)

    for i in range(4):
        gpio.set_pin_as_output(__GPIO_PIN_MUL_LED_IN_ADDRESS_START__ + i)
        gpio.set_pin_as_output(__GPIO_PIN_MUL_LED_OUT_ADDRESS_START__ + i)

    write_address_in(0)
    write_address_out(0)

    gpio.set_pin_as_output(__GPIO_PIN_EXTRA_LED_IN_1__)
    gpio.set_pin_as_output(__GPIO_PIN_EXTRA_LED_IN_2__)
    gpio.set_pin_as_output(__GPIO_PIN_EXTRA_LED_IN_3__)

    gpio.set_pin_low(__GPIO_PIN_EXTRA_LED_IN_1__)
    gpio.set_pin_low(__GPIO_PIN_EXTRA_LED_IN_2__)
    gpio.set_pin_low(__GPIO_PIN_EXTRA_LED_IN_3__)

    gpio.set_pin_as_output(__GPIO_PIN_EXTRA_LED_OUT_1__)
    gpio.set_pin_as_output(__GPIO_PIN_EXTRA_LED_OUT_2__)
    gpio.set_pin_as_output(__GPIO_PIN_EXTRA_LED_OUT_3__)

    gpio.set_pin_low(__GPIO_PIN_EXTRA_LED_OUT_1__)
    gpio.set_pin_low(__GPIO_PIN_EXTRA_LED_OUT_2__)
    gpio.set_pin_low(__GPIO_PIN_EXTRA_LED_OUT_3__)