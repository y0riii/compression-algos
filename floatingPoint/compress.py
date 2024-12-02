import json

def compress(inputFile: str, outputFile: str):
    with open(inputFile, "r") as file:
        data = file.read()
    result = {}
    chars = sorted(set(data))
    size = len(data)
    probabilities = {char: data.count(char) / size for char in chars}
    ranges = {}
    last = 0
    for key, prob in probabilities.items():
        ranges[key] = (last, last + prob)
        last += prob
    currentRange = (0, 1)
    for char in data:
        range = currentRange[1] - currentRange[0]
        lower = currentRange[0] + range * ranges[char][0]
        upper = currentRange[0] + range * ranges[char][1]
        currentRange = (lower, upper)
    result["compressed"] = (currentRange[0] + currentRange[1]) / 2
    result["probabilities"] = probabilities
    result["size"] = size
    with open(outputFile, "w") as file:
        json.dump(result, file, indent=4)
