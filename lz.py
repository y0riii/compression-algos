# s = "ABAABABAABBBBBBBBBBBBA"
# s = "ABAABABABABABABABABABA"
s = "CABRACADABRARRARRADDD"

def compress(data):
    n = len(data)
    windowSize = max(n // 2, 10)
    bufferSize = windowSize
    res = []
    i = 0

    while i < n:
        matchOffset = 0
        matchLength = 0
        lookahead = min(bufferSize, n - i - 1)

        for j in range(1, min(windowSize, i) + 1):
            length = 0
            while (length < lookahead and 
                   data[i - j + length] == data[i + length]):
                length += 1

            if length > matchLength:
                matchLength = length
                matchOffset = j

        nextChar = data[i + matchLength]
        res.append((matchOffset, matchLength, nextChar))
        i += matchLength + 1

    return res

def deCompress(res_data):
    res = []

    for offset, length, char in res_data:
        start = len(res) - offset
        for i in range(length):
            res.append(res[start + i])
        res.append(char)

    return ''.join(res)        
              

compressed = compress(s)
print(compressed)

decompressed = deCompress(compressed)
print(decompressed)
print(decompressed == s)
