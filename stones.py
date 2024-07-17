import time
import gpio
import logging

__GPIO_PIN_MUL_EN_1_IN__ = 17
__GPIO_PIN_MUL_EN_2_IN__ = 18
__GPIO_PIN_MUL_EN_1_OUT__ = 6
__GPIO_PIN_MUL_EN_2_OUT__ = 7
__GPIO_PIN_MUL_STONES_IN_ADDRESS__ = [13, 14, 15, 16]
__GPIO_PIN_MUL_STONES_OUT_ADDRESS__ = [1, 2, 3, 5]
__GPIO_PIN_STONES_OUT__ = 9
__GPIO_MUL_ADDRESS_SIZE__ = 4
__GPIO_MUL_MAX_ADDRESS__= 16
__GPIO_BOARD_SIZE__ = 19

__READ_DELAY_SECONDS__ = 0.05

def write_address(address: int, direction_out: bool):
    if address >= __GPIO_BOARD_SIZE__ or address < 0:
        logging.critical("Invalid address" + str(address))
        return
    direction_string = ""
    multiplexer_string = ""
    if address >= __GPIO_MUL_MAX_ADDRESS__:
        multiplexer_string = "2"
        address -= __GPIO_MUL_MAX_ADDRESS__
        if direction_out:
            direction_string = "OUT"
            gpio.set_pin_high(__GPIO_PIN_MUL_EN_1_OUT__)
            gpio.set_pin_low(__GPIO_PIN_MUL_EN_2_OUT__)
        else:
            direction_string = "IN"
            gpio.set_pin_high(__GPIO_PIN_MUL_EN_1_IN__)
            gpio.set_pin_low(__GPIO_PIN_MUL_EN_2_IN__)
    else:
        multiplexer_string = "1"
        if direction_out:
            direction_string = "OUT"
            gpio.set_pin_low(__GPIO_PIN_MUL_EN_1_OUT__)
            gpio.set_pin_high(__GPIO_PIN_MUL_EN_2_OUT__)
        else:
            direction_string = "IN"
            gpio.set_pin_low(__GPIO_PIN_MUL_EN_1_IN__)
            gpio.set_pin_high(__GPIO_PIN_MUL_EN_2_IN__)
    logging.info("Writing Address " 
                 + direction_string + " to " 
                 + str(address) + ", using Multiplexer " 
                 + multiplexer_string)
    write_address_8(address, direction_out)


def write_address_8(address: int, direction_out: bool):
    address_array = __GPIO_PIN_MUL_STONES_OUT_ADDRESS__ if direction_out else __GPIO_PIN_MUL_STONES_IN_ADDRESS__
    current_address_bit = 1
    for i in range(__GPIO_MUL_ADDRESS_SIZE__):
        set_to = "error"
        if address & current_address_bit:
            set_to = "high"
            gpio.set_pin_high(address_array[i]) # counting from zero
        else:
            set_to = "low"
            gpio.set_pin_low(address_array[i]) # counting from zero
            
        logging.debug("Setting Pin with adress index " + str(i) 
                    + ", linear ID " + str(address_array[i])
                    + ", GPIO ID " + str(gpio.get_inverted_mapped_value(address_array[i]))
                    + " to " + set_to)
        current_address_bit = current_address_bit << 1


def init_stones():
    gpio.gpio_init_mode()

    for i in range(__GPIO_MUL_ADDRESS_SIZE__):
        gpio.set_pin_as_output(__GPIO_PIN_MUL_STONES_IN_ADDRESS__[i])
        gpio.set_pin_as_output(__GPIO_PIN_MUL_STONES_OUT_ADDRESS__[i])

    gpio.set_pin_as_output(__GPIO_PIN_MUL_EN_1_IN__)
    gpio.set_pin_as_output(__GPIO_PIN_MUL_EN_2_IN__)
    gpio.set_pin_as_output(__GPIO_PIN_MUL_EN_1_OUT__)
    gpio.set_pin_as_output(__GPIO_PIN_MUL_EN_2_OUT__)
    gpio.set_pin_as_input(__GPIO_PIN_STONES_OUT__)

    write_address(0, True)
    write_address(0, False)
    logging.warning("Finished initialising stones")


def get_stones() -> list[(int, int)]:
    stones = list()
    for x in range(__GPIO_BOARD_SIZE__):
        for y in range(__GPIO_BOARD_SIZE__):
            if get_stone(x, y):
                stones += [(x, y)]
    return stones

def get_stone(x: int, y: int) -> bool:
    write_address(x, True)
    write_address(y, False)
    time.sleep(__READ_DELAY_SECONDS__)
    is_stone = gpio.read_pin(__GPIO_PIN_STONES_OUT__)
    stone_string = "" if is_stone else "NO "
    logging.info("Detected " + stone_string + " stone at x=" + str(x) + ", y=" + str(y))
    return 