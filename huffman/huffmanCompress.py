from queue import PriorityQueue
import json


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
    huffDict = {}

    if (node.left):
        huffDict.update(getDict(node.left, huff + "0"))
    if (node.right):
        huffDict.update(getDict(node.right, huff + "1"))
    if (not node.left and not node.right):
        huffDict[node.symbol] = huff
    return huffDict


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
    huffDict = getDict(pq.get()[1])
    huffDict = dict(sorted(huffDict.items()))
    compressed = ""
    for char in data:
        compressed += huffDict[char]
    huffDict = {value: key for key, value in huffDict.items()}
    return (compressed, huffDict)


def writeBinaryFile(fileName, binaryString):
    binaryString = '1' + binaryString
    number = int(binaryString, 2)
    byte_data = number.to_bytes((len(binaryString) + 7) // 8, byteorder='big')
    with open(fileName, 'wb') as f:
        f.write(byte_data)


with open("input.txt", "r") as file:
    string = file.read()

compressed, huffDict = huffmanCompress(string)
writeBinaryFile("compressed.bin", compressed)

with open("huffDict.json", 'w') as file:
    json.dump(huffDict, file)
