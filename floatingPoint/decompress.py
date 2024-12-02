import json


def decompress(inputFile: str, outputFile: str):
    with open(inputFile, "r") as file:
        data: dict = json.load(file)
    value = data["compressed"]
    ranges = {}
    last = 0
    for key, prob in data["probabilities"].items():
        ranges[key] = (last, last + prob)
        last += prob
    result = ""
    currentRange = (0, 1)
    for _ in range(data["size"]):
        Range = currentRange[1] - currentRange[0]
        value = (value - currentRange[0]) / Range
        for key, (lower, upper) in ranges.items():
            if lower <= value < upper:
                result += key
                currentRange = (lower, upper)
                break
    with open(outputFile, "w") as file:
        file.write(result)
