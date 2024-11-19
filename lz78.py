s = "ABAABABAABABBBBBBBBBBA"
# s = "ABAABABABABABABABABABA"
# s = "CABRACADABRARRARRADDD"


def compress(data):
    dictionary = ["", data[0]]
    compressed = [(0, data[0])]

    i = 1
    n = len(data)
    while i < n:
        j = i + 1
        while j < n and data[i:j] in dictionary:
            j += 1
        char = data[j - 1]
        index = dictionary.index(data[i:j - 1])
        compressed.append((index, char))
        dictionary.append(data[i:j])
        i = j
    return compressed


def decompress(data):
    dictionary = [""]
    decompressed = []
    for index, char in data:
        string = dictionary[index] + char
        dictionary.append(string)
        decompressed.append(string)
    return "".join(decompressed)

compressed = compress(s)
print(compressed)
decompressed = decompress(compressed)
print(decompressed)
print(decompressed == s)
