#! /usr/bin/python3

import time
import stones, gpio, pins_to_linear
# import leds
import argparse

__MAX_BOARDSIZE__ = 19

def loop():
    # stones_list = get_stones()
    stones_list = stones.get_stones()
    print_board(stones_list)

adress_size = 4
address_array = [23, 24, 25, 27]
output_array = [14, 15, 16, 17, 18]

def main():
    args = handle_args()
    gpio.gpio_init_mode()

    address = 0
    init_lines()

    if args.test:
        print("Testing Multiplexer output " + str(args.test))

        write_address(args.test)

        time.sleep(1)

        read_output_pins()

        time.sleep(20)
        gpio.gpio_deinit()
        exit(0)


    while True:
        print("Testing Multiplexer output " + str(address))

        # init_lines()

        write_address(address)

        time.sleep(1)

        read_output_pins()
        
        # pull_down_lines()


        time.sleep(1)
        address += 1
        if address == 16:
            address = 0

    gpio.gpio_deinit()

    """
    global size

    size = args.size
    # init_stones()
    stones.init_stones()

    while True:
        loop()
        time.sleep(0.5)
    """

def write_address(address):
    current_address_bit = 1
    for i in range(adress_size):
        set_to = "error"
        if address & current_address_bit:
            set_to = "high"
            gpio.set_pin_high(pins_to_linear.get_inverted_mapped_value(address_array[i])) # counting from zero
        else:
            set_to = "low"
            gpio.set_pin_low(pins_to_linear.get_inverted_mapped_value(address_array[i])) # counting from zero
            
        print("Setting Pin with adress index " + str(i) 
                    + ", linear ID " + str(address_array[i])
                    + ", GPIO ID " + str(pins_to_linear.get_inverted_mapped_value(address_array[i]))
                    + " to " + set_to)
        print(current_address_bit)
        print(address & current_address_bit)
        current_address_bit = current_address_bit << 1

def read_output_pins():
    for output in output_array:
        level = ""
        if gpio.read_pin(pins_to_linear.get_inverted_mapped_value(output)):
            level = "high"
        else:
            level = "low"
        print("Channel " + str(output) + " is " + level)
def init_lines():
    for i in range(adress_size):
        gpio.set_pin_as_output(pins_to_linear.get_inverted_mapped_value(address_array[i]))

    for output in output_array:
        gpio.set_pin_as_input(pins_to_linear.get_inverted_mapped_value(output))
    
def pull_down_lines():
    for key in pins_to_linear.pin_to_linear_mapping:
        gpio.set_pin_as_output(key)
        gpio.set_pin_low(key)

def print_board(stones_list: list[(int, int)]):
    start = int((__MAX_BOARDSIZE__ - size) / 2)
    end = start + size
    for y in range(size):
        print("\t" + str(y + 1), end="")
        
    for x in range(start, end):
        print("\n" + str(x + 1) + "\t", end="")
        for y in range(start, end):
            if (x, y) in stones_list:
                print("X", end="\t")
            else:
                print(" ", end="\t")
    print()

def handle_args():
    parser = argparse.ArgumentParser(description="Test script for the Go-Board")
    parser.add_argument("-s", "--size", type=int, choices=[9, 13, __MAX_BOARDSIZE__], default=__MAX_BOARDSIZE__,
                        help="Size of milliseconds to wait. Default is " + str(__MAX_BOARDSIZE__) + ", also accepts 9 and 13.")
    parser.add_argument("-t", "--test", type=int, help="Test by setting the given GPIO Pin high")
    return parser.parse_args()
"""
def init_stones():
    return

def get_stones():
    stones_list = list()
    for x in range(__MAX_BOARDSIZE__):
        for y in range(__MAX_BOARDSIZE__):
            if random.random() < 0.1:
                stones_list += [(x, y)]
    return stones_list
"""

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        print("Keyboard interrupt")

    finally:
        print("clean up") 
    gpio.gpio_deinit()