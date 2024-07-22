#! /usr/bin/python3

import random
import time
import stones, gpio
# import leds
import argparse
import logging

__MAX_BOARDSIZE__ = 19

def loop():
    # stones_list = get_stones()
    stones_list = stones.get_stones()
    logging.info(str(stones_list))
    print_board(stones_list)


# Map the verbosity level to the logging level
verbosity_levels = {
    0: logging.CRITICAL,
    1: logging.ERROR,
    2: logging.WARNING,
    3: logging.INFO,
    4: logging.DEBUG
}


def main():
    args = handle_args()

    global size
    size = args.size
    
    # Set the logging level
    logging_level = verbosity_levels.get(args.verbosity, logging.DEBUG)

    # Configure logging
    logging.basicConfig(level=logging_level,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(args.output)])

    
    stones.init_stones()

    if args.test:
        address = args.test
        print("Testing Multiplexer address " + str(address))

        stones.write_address(15 - address, False) # in
        stones.write_address(address, True) # out

        time.sleep(1)

        for i in range(40):
            signal = gpio.read_pin(stones.__GPIO_PIN_STONES_OUT__)
            print("Signal is " + ("high" if signal else "low"))
            time.sleep(1)
            
        gpio.gpio_deinit()
        exit(0)


    stones.init_stones()
    
    loop_counter = 0
    while True:
        logging.warning("Running Loop " + str(loop_counter))
        loop()
        # time.sleep(10)
        loop_counter += 1
    

def print_board(stones_list: list[(int, int)]):
    print()
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
    parser.add_argument('-v', '--verbosity', type=int, choices=range(0, 5),
                    default=5, help='Set the logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG')
    parser.add_argument('-o', '--output', type=str, default='go_board.log', help='Set the logging output file')

    return parser.parse_args()

def get_stones():
    stones_list = list()
    for x in range(__MAX_BOARDSIZE__):
        for y in range(__MAX_BOARDSIZE__):
            if random.random() < 0.1:
                stones_list += [(x, y)]
    return stones_list

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        print("Keyboard interrupt")

    finally:
        print("clean up") 
    gpio.gpio_deinit()