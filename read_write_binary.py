def write_binary_file(filename, binary_string):
    binary_string = '1' + binary_string
    # Convert binary string to bytes
    number = int(binary_string, 2)
    byte_data = number.to_bytes((len(binary_string) + 7) // 8, byteorder='big')

    # Open file in binary write mode
    with open(filename, 'wb') as f:
        f.write(byte_data)


def read_binary_file(filename):

    with open(filename, 'rb') as f:
        byte_data = f.read()

    return bin(int.from_bytes(byte_data, byteorder='big'))[3:]


# Example usage
binary_string = '00000010'  # You can replace this with any binary string
write_binary_file('binary_file.bin', binary_string)

value = read_binary_file('binary_file.bin')
print(value)
