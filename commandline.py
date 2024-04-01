#! /usr/bin/python3

import time
# import stones, leds
import argparse
import random


__MAX_BOARDSIZE__ = 19

def loop():
    stones_list = get_stones()
    # stones_list = stones.get_stones()
    print_board(stones_list)

def main():
    args = handle_args()
    global size

    size = args.size
    init_stones()
    # stones.init_stones()

    while True:
        loop()
        time.sleep(0.5)
    
def print_board(stones_list: list[(int, int)]):
    start = int((__MAX_BOARDSIZE__ - size) / 2)
    end = start + size
    for y in range(size):
        print(y + 1, end="")
    print()
        
    for x in range(start, end):
        print("\n" + str(x + 1) + "\t", end="")
        for y in range(start, end):
            if (x, y) in stones_list:
                print("X", end="")
            else:
                print(" ", end="")

def handle_args():
    parser = argparse.ArgumentParser(description="Test script for the Go-Board")
    parser.add_argument("-s", "--size", type=int, choices=[9, 13, __MAX_BOARDSIZE__], default=__MAX_BOARDSIZE__,
                        help="Size of milliseconds to wait. Default is " + str(__MAX_BOARDSIZE__) + ", also accepts 9 and 13.")
    return parser.parse_args()

def init_stones():
    return

def get_stones():
    stones_list = list()
    for x in range(__MAX_BOARDSIZE__):
        for y in range(__MAX_BOARDSIZE__):
            if random.random() < 0.1:
                stones_list += [(x, y)]
    return stones_list


if __name__ == "__main__":
    main()