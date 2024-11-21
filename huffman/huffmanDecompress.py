import json
import filecmp


def hummanDecompress(compressed: str, huffDict: dict):
    decompressed = ""
    temp = ""
    for char in compressed:
        temp += char
        if temp in huffDict:
            decompressed += huffDict[temp]
            temp = ""
    return decompressed


def readBinaryFile(fileName):
    with open(fileName, 'rb') as f:
        byte_data = f.read()
    return bin(int.from_bytes(byte_data, byteorder='big'))[3:]


compressed = readBinaryFile("compressed.bin")
with open("huffDict.json", "r") as file:
    huffDict = json.load(file)

decompressed = hummanDecompress(compressed, huffDict)

with open("output.txt", "w") as file:
    file.write(decompressed)

print(filecmp.cmp("input.txt", "output.txt"))
