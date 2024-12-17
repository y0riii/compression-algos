import json
import cv2
import numpy as np


def decompress(compressed_file, output_path):
    with open(compressed_file, 'r') as file:
        data = json.load(file)
    rows, cols = data['shape']
    block_size = data['blockSize']
    code_book = np.array(data['codeBook'], dtype=np.uint8)
    vectors = data['vectors']
    block_shape = (block_size, block_size)
    reconstructed_image = np.zeros((rows, cols), dtype=np.uint8)
    pad_rows = (block_size - (rows % block_size)) % block_size
    pad_cols = (block_size - (cols % block_size)) % block_size

    padded_shape = (rows + pad_rows, cols + pad_cols)

    reconstructed_image = np.zeros(padded_shape, dtype=np.uint8)
    vector_idx = 0
    for i in range(0, padded_shape[0], block_size):
        for j in range(0, padded_shape[1], block_size):
            codebook_vector = code_book[vectors[vector_idx]]
            block = codebook_vector.reshape(block_shape)

            reconstructed_image[i:i + block_size, j:j + block_size] = block

            vector_idx += 1
    final_image = reconstructed_image[:rows, :cols]
    cv2.imwrite(output_path, final_image)


if __name__ == "__main__":
    compressed_file = "compressed.json"
    output_path = "decompressed.png"
    decompress(compressed_file, output_path)
