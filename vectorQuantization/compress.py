import json
import cv2
import numpy as np


def image_to_matrix(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Error: Unable to load image. Check the file path.")
    return img


def get_vectors(matrix, block_size):
    rows, cols = matrix.shape

    pad_rows = (block_size - (rows % block_size)) % block_size
    pad_cols = (block_size - (cols % block_size)) % block_size

    padded_matrix = np.pad(matrix, ((0, pad_rows), (0, pad_cols)), mode='edge')

    vectors = []

    for i in range(0, rows, block_size):
        for j in range(0, cols, block_size):
            submatrix = padded_matrix[i:i+block_size, j:j+block_size]
            vectors.append(submatrix.flatten())
    vectors = [(vectors[i], i) for i in range(len(vectors))]
    return vectors


def get_average(vectorsGroup):
    vectors = [v[0] for v in vectorsGroup]
    vectors = np.array(vectors)
    return np.mean(vectors, axis=0).tolist()


def go_left(avrageVector, vector2):
    countPositive = 0
    countNegative = 0
    for i in range(len(avrageVector)):
        if vector2[i] < avrageVector[i]:
            countPositive += 1
        else:
            countNegative += 1
    return countPositive > countNegative


def get_code_book(vectors, book_size):
    if book_size == 1 or len(vectors) == 1:
        return [vectors]

    vectorAverage = get_average(vectors)

    left = []
    right = []

    for vector in vectors:
        if go_left(vectorAverage, vector[0]):
            left.append(vector)
        else:
            right.append(vector)
    if len(left) == 0:
        return get_code_book(right, book_size)
    left_code_book = get_code_book(left, book_size // 2)
    right_code_book = get_code_book(right, book_size - len(left_code_book))
    return left_code_book + right_code_book


def compress(image_path, output_file, block_size, book_size):
    matrix = image_to_matrix(image_path)
    vectors = get_vectors(matrix, block_size)
    code_book = get_code_book(vectors, book_size)
    q = [0] * len(vectors)
    averages = []
    for i in range(len(code_book)):
        averageVector = get_average(code_book[i])
        averageVector = [round(x) for x in averageVector]
        averages.append(averageVector)
        for vector in code_book[i]:
            q[vector[1]] = i
    compressed = {}
    compressed["shape"] = matrix.shape
    compressed["blockSize"] = block_size
    compressed["codeBook"] = averages
    compressed["vectors"] = q
    with open(output_file, "w") as json_file:
        json.dump(compressed, json_file)


if __name__ == "__main__":
    image_path = "img.jpg"
    output_file = "compressed.json"
    block_size = 4
    book_size = 32

    try:
        compress(image_path, output_file, block_size, book_size)

    except Exception as e:
        with open(output_file, "w") as f:
            f.write(f"Error: {str(e)}\n")
        print(f"Error occurred: {str(e)}")
