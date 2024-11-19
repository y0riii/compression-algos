from queue import PriorityQueue


class Node:
    def __init__(self, left=None, right=None, symbol=""):
        self.left = left
        self.right = right
        if (left and right):
            self.symbol = left.symbol + right.symbol
        else:
            self.symbol = symbol

    def __lt__(self, other):
        return self.symbol < other.symbol


def getDict(node, huff=""):
    huff_dict = {}

    if (node.left):
        huff_dict.update(getDict(node.left, huff + "1"))
    if (node.right):
        huff_dict.update(getDict(node.right, huff + "0"))
    if (not node.left and not node.right):
        huff_dict[node.symbol] = huff
    return huff_dict


def huffmanCompress(data: str):
    pq = PriorityQueue()
    chars = set(data)
    for char in chars:
        pq.put((data.count(char), Node(symbol=char)))
    for _ in range(len(chars) - 1):
        left = pq.get()
        right = pq.get()
        freq = left[0] + right[0]
        pq.put((freq, Node(left[1], right[1])))
    huff_dict = getDict(pq.get()[1])
    huff_dict = dict(sorted(huff_dict.items()))
    compressed = ""
    for char in data:
        compressed += huff_dict[char]
    return (compressed, huff_dict)

def hummanDecompress(compressed: str, huff_dict: dict):
    reversed_huff_dict = {value: key for key, value in huff_dict.items()}
    decompressed = ""
    temp = ""
    for char in compressed:
        temp += char
        if temp in reversed_huff_dict:
            decompressed += reversed_huff_dict[temp]
            temp = ""
    return decompressed

s = "CABRACADABRARRARRRRRRRRRADDD"
compressed, huff_dict = huffmanCompress(s)
print(compressed)
print(huff_dict)
decompressed = hummanDecompress(compressed, huff_dict)
print(decompressed)
print(decompressed == s)

