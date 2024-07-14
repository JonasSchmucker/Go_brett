# Define the original static dictionary that maps numbers to numbers
pin_to_linear_mapping = {
    # 3V
    2: 1,
    3: 2,
    4: 3,
    # GND
    17: 5,
    27: 6,
    22: 7,
    # 3V
    10: 9,
    9: 10,
    11: 11,
    # GND
    0: 13,
    5: 14,
    6: 15,
    13: 16,
    19: 17,
    26: 18,
    # GND

    # 5V
    # 5V
    # GND
    14: 23,
    15: 24,
    18: 25,
    # GND
    23: 27,
    24: 28,
    # GND
    25: 30,
    8: 31, 
    7: 32,
    1: 33,
    # GND
    12: 35,
    # GND
    16: 37,
    20: 38,
    21: 39
}

# Function to invert the bijective mapping
def invert_mapping(mapping):
    return {value: key for key, value in mapping.items()}

# Invert the original mapping
linear_to_pin_mapping = invert_mapping(pin_to_linear_mapping)

# Function to get the mapped value from the inverted mapping
def get_inverted_mapped_value(key):
    return linear_to_pin_mapping.get(key, "Key not found")

# Function to get the mapped value
def get_mapped_value(key):
    return pin_to_linear_mapping.get(key, "Key not found")

# Test the function
if __name__ == "__main__":
    test_keys = [1, 5, 10, 11]
    for key in test_keys:
        print(f"Key: {key}, Mapped Value: {get_mapped_value(key)}")
        print(f"Key: {key}, Inverted Mapped Value: {get_inverted_mapped_value(key)}")
