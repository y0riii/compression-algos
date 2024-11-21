def compress(date, probabilities: dict):
    probabilities = dict(sorted(probabilities.items()))
    ranges = {}
    last = 0
    for key, prob in probabilities.items():
        ranges[key] = (last, last + prob)
        last += prob
    currentRange = (0, 1)
    for char in date:
        range = currentRange[1] - currentRange[0]
        lower = currentRange[0] + range * ranges[char][0]
        upper = currentRange[0] + range * ranges[char][1]
        currentRange = (lower, upper)
    return (currentRange[0] + currentRange[1]) / 2


def decompress(value, probabilities: dict, numberOfChars: int):
    probabilities = dict(sorted(probabilities.items()))
    ranges = {}
    last = 0
    for key, prob in probabilities.items():
        ranges[key] = (last, last + prob)
        last += prob
    date = ""
    currentRange = (0, 1)
    for _ in range(numberOfChars):
        Range = currentRange[1] - currentRange[0]
        value = (value - currentRange[0]) / Range
        for key, (lower, upper) in ranges.items():
            if lower <= value < upper:
                date += key
                currentRange = (lower, upper)
                break
    return date


commpressed = compress("AABCBACC", {'A': 0.8, 'B': 0.02, 'C': 0.18})
print(commpressed)
date = decompress(commpressed, {'A': 0.8, 'B': 0.02, 'C': 0.18}, 8)
print(date)
