import time
import gpio

__GPIO_PIN_MUL_EN_1_IN__ = 27
__GPIO_PIN_MUL_EN_2_IN__ = 14
__GPIO_PIN_MUL_EN_1_OUT__ = 11
__GPIO_PIN_MUL_EN_2_OUT__ = 15
__GPIO_PIN_MUL_STONES_IN_ADDRESS_START__ = 2  # 2, 3, 4 #(S3 Address)  EN1 S0 S1 S2 S3 EN2
__GPIO_PIN_MUL_STONES_OUT_ADDRESS_START__ = 7 # 7, 8, 9, # S3 is MSB
__GPIO_PIN_STONES_IN_ADDRESS__ = 25
__GPIO_MUL_ADDRESS_SIZE__ = 4
__GPIO_MUL_MAX_ADDRESS__= 16
__GPIO_BOARD_SIZE__ = 19

def write_address(address: int, direction_out: bool):
    if address >= __GPIO_BOARD_SIZE__ or address < 0:
        print("Invalid address" + str(address))
        return
    if address >= __GPIO_MUL_MAX_ADDRESS__:
        address -= __GPIO_MUL_MAX_ADDRESS__
        if direction_out:
            gpio.set_pin_high(__GPIO_PIN_MUL_EN_1_OUT__)
            gpio.set_pin_low(__GPIO_PIN_MUL_EN_2_OUT__)
        else:
            gpio.set_pin_high(__GPIO_PIN_MUL_EN_1_IN__)
            gpio.set_pin_low(__GPIO_PIN_MUL_EN_2_IN__)
    else:
        if direction_out:
            gpio.set_pin_low(__GPIO_PIN_MUL_EN_1_OUT__)
            gpio.set_pin_high(__GPIO_PIN_MUL_EN_2_OUT__)
        else:
            gpio.set_pin_low(__GPIO_PIN_MUL_EN_1_IN__)
            gpio.set_pin_high(__GPIO_PIN_MUL_EN_2_IN__)
    write_address_8(address, direction_out)


def write_address_8(address: int, direction_out: bool):
    address_base = __GPIO_PIN_MUL_STONES_OUT_ADDRESS_START__ if direction_out else __GPIO_PIN_MUL_STONES_IN_ADDRESS_START__ 
    if address >= __GPIO_MUL_MAX_ADDRESS__ or address < 0:
        print("Invalid address" + str(address))
        return
    
    current_address_bit = 1
    for i in range(__GPIO_MUL_ADDRESS_SIZE__):
        if address & current_address_bit:
            gpio.set_pin_high(address_base + i) # counting from zero
        else:
            gpio.set_pin_low(address_base + i) # counting from zero
        current_address_bit << 1


def init_stones():
    gpio.gpio_init_mode()

    for i in range(__GPIO_MUL_ADDRESS_SIZE__):
        gpio.set_pin_as_output(__GPIO_PIN_MUL_STONES_IN_ADDRESS_START__ + i)
        gpio.set_pin_as_output(__GPIO_PIN_MUL_STONES_OUT_ADDRESS_START__ + i)

    write_address(0, True)
    write_address(0, False)


def get_stones() -> list[(int, int)]:
    stones = list()
    for x in range(__GPIO_MUL_MAX_ADDRESS__):
        for y in range(__GPIO_MUL_MAX_ADDRESS__):
            if get_stone(x, y):
                stones += [(x, y)]
    return stones

def get_stone(x: int, y: int) -> bool:
    write_address(x, True)
    write_address(y, False)
    time.sleep(0.001)
    return gpio.read_pin(__GPIO_PIN_STONES_IN_ADDRESS__)