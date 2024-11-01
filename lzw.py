DICTIONARY = [chr(i) for i in range(128)]

def lzw_compress(data):
    compressionDict = DICTIONARY.copy()
    result = []
    foundChars = ''
    for char in data:
        searchString = foundChars + char
        if searchString in compressionDict:
            foundChars = searchString
        else:
            result.append(compressionDict.index(foundChars))
            compressionDict.append(searchString)
            foundChars = char
    result.append(compressionDict.index(foundChars))
    return result


def lzw_decompress(data: list):
    decompressionDict = DICTIONARY.copy()
    privious = decompressionDict[data.pop(0)]
    result = privious
    for index in data:
        if index < len(decompressionDict):
            current = decompressionDict[index]
        else:
            current = privious + privious[0]
        result += current
        decompressionDict.append(privious + current[0])
        privious = current
    return result

s = input()

compressed = lzw_compress(s)
print(compressed)

decompressed = lzw_decompress(compressed)
print(decompressed)

print(s == decompressed)