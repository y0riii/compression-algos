import cv2
import numpy as np

Code_Book_Size = 64
Loops = 6
Block_Size = 5
Width = 0
Height = 0
my_sub_matrix = []
my_index = []

def image_to_matrix(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Error: Unable to load image. Check the file path.")
    return img

def matrix_to_image(matrix, output_path):
    if not isinstance(matrix, np.ndarray) or len(matrix.shape) != 2:
        raise ValueError("Error: Input must be a 2D numpy array.")
    success = cv2.imwrite(output_path, matrix)
    if not success:
        raise ValueError("Error: Unable to save the image. Check the output path.")

def get_vectors(matrix):
    global my_sub_matrix, my_index
    rows, cols = matrix.shape
    submatrices = []
    
    my_sub_matrix = np.zeros((rows, cols), dtype=int)
    my_index = np.zeros((rows, cols), dtype=int)
    
    for i in range(0, rows, Block_Size):
        for j in range(0, cols, Block_Size):
            submatrix = matrix[i:i+Block_Size, j:j+Block_Size]
            cnt = 0
            for x in range(Block_Size):
                for y in range(Block_Size):
                    if i + x < rows and j + y < cols:
                        my_sub_matrix[i + x][j + y] = len(submatrices)
                        my_index[i + x][j + y] = cnt
                        cnt += 1

            if submatrix.shape == (Block_Size, Block_Size):
                submatrices.append(submatrix)
    
    return submatrices

def get_average(group):
    avg_matrix = np.zeros((Block_Size, Block_Size))
    
    for g in group:
        for i in range(Block_Size):
            for j in range(Block_Size):
                avg_matrix[i][j] += g[i][j]  
    group_size = len(group)
    if group_size:
        avg_matrix /= group_size 
    return avg_matrix

def get_distance(matrix1, matrix2):
    sum = 0
    for i in range(Block_Size):
        for j in range(Block_Size):
            sum += (matrix1[i][j] - matrix2[i][j]) ** 2
    return sum

my_code_book = []
def get_code_book(submatrices):
    avg_matrix = get_average(submatrices)
    code_book = []
    code_book.append(avg_matrix)
    
    for i in range(Loops):
        cur_code_book = []
        my_code_book.clear()
        for book in code_book:
            book1 = np.ceil(book)
            book2 = np.floor(book)
            
            cur_code_book.append(book1)
            cur_code_book.append(book2)
        
        groups = [[] for _ in range(len(cur_code_book))]
    
        for submatrix in submatrices:
            min_dist = 1e18
            idx = -1
            for i in range(len(cur_code_book)):  
                cur_dist = get_distance(submatrix, cur_code_book[i])
                if cur_dist < min_dist:
                    min_dist = cur_dist
                    idx = i
            groups[idx].append(submatrix)  
            my_code_book.append(idx)

        code_book = []
        for g in groups:  
            code_book.append(get_average(g))    

    return code_book    

def compress(submatrices):
    compressed = np.zeros((len(submatrices),), dtype=int)
    i = 0
    for sub in submatrices:
        compressed[i] = my_code_book[i]
        i += 1    
    return compressed

def decompressed_matrix(code_book):
    global my_sub_matrix, my_index
    rows, cols = my_sub_matrix.shape
    decompressed =  np.zeros((rows, cols), dtype=int)
    
    for i in range(rows):
        for j in range(cols):
            idx = my_code_book[my_sub_matrix[i][j]]
            if idx < len(code_book):
                decompressed[i][j] = code_book[idx][my_index[i][j] // Block_Size][my_index[i][j] % Block_Size]
            else:
                print(f"Index {idx} is out of bounds for codebook.")
    
    return decompressed


if __name__ == "__main__":
    image_path = "img.jpg"  
    output_file = "output.txt"  

    try:
        matrix = image_to_matrix(image_path)
        split_matrix = get_vectors(matrix)
        code_book = get_code_book(split_matrix)
        compressed_matrix = compress(split_matrix)
        Width = matrix.shape[1]
        Height = matrix.shape[0]
        
        decompressed_matrix_result = decompressed_matrix(code_book)
        
        matrix_to_image(decompressed_matrix_result, "decompressed_image.png")

        with open(output_file, "w") as f:
            
            f.write("\nCompressed Matrix (indices of closest codebook):\n")
            np.savetxt(f, compressed_matrix, fmt="%d")
            
            f.write("\nCodebook:\n")
            for idx, matrix in enumerate(code_book):
                f.write(f"Codebook Matrix {idx+1}:\n")
                np.savetxt(f, matrix, fmt="%d")
                f.write("\n")

            f.write("\nDecompressed Matrix (reconstructed image):\n")
            np.savetxt(f, decompressed_matrix_result, fmt="%d")    
        
        print("Process completed successfully. Check output.txt for details.")

    except Exception as e:
        with open(output_file, "w") as f:
            f.write(f"Error: {str(e)}\n")
        print(f"Error occurred: {str(e)}")
