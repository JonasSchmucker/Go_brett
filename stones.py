import gpio

__GPIO_PIN_MUL_STONES_IN_ADDRESS_START__ = 0
__GPIO_PIN_MUL_STONES_OUT_ADDRESS_START__ = 0
# __GPIO_PIN_STONES_OUT_ADDRESS__ = 0
__GPIO_PIN_STONES_IN_ADDRESS__ = 0
__GPIO_PIN_MUL_ADDRESS_SIZE__ = 5
__GPIO_PIN_MUL_MAX_ADDRESS__= 19

def write_address(address: int, direction_out: bool):
    address_base = __GPIO_PIN_MUL_STONES_OUT_ADDRESS_START__ if direction_out else __GPIO_PIN_MUL_STONES_IN_ADDRESS_START__ 
    if address >= __GPIO_PIN_MUL_MAX_ADDRESS__ or address < 0:
        print("Invalid address" + str(address))
        return
    
    current_address_bit = 1
    for i in range(__GPIO_PIN_MUL_MAX_ADDRESS__):
        if address & current_address_bit:
            gpio.set_pin_high(address_base + i) # counting from zero
        else:
            gpio.set_pin_low(address_base + i) # counting from zero
        current_address_bit << 1


def init_stones():
    for i in range(__GPIO_PIN_MUL_ADDRESS_SIZE__):
        gpio.set_pin_as_output(__GPIO_PIN_MUL_STONES_IN_ADDRESS_START__ + i)
        gpio.set_pin_as_output(__GPIO_PIN_MUL_STONES_OUT_ADDRESS_START__ + i)

    write_address(0, True)
    write_address(0, False)


def get_stones() -> list[(int, int)]:
    stones = list()
    for x in range(__GPIO_PIN_MUL_MAX_ADDRESS__):
        for y in range(__GPIO_PIN_MUL_MAX_ADDRESS__):
            if get_stone(x, y):
                stones += [(x, y)]
    return stones

def get_stone(x: int, y: int) -> bool:
    write_address(x, True)
    write_address(y, False)
    return gpio.read_pin(__GPIO_PIN_STONES_IN_ADDRESS__)