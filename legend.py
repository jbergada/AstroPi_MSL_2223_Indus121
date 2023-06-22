import numpy as np
import cv2
from fastiecm import fastiecm

# Create a matrix with 200 rows and 10 columns
bits = 255
matrix = np.zeros((bits, 100, 3), dtype=np.uint8)

# Filling the matrix with groups of numbers from 0 to 255
for i in range(bits):
    for j in range(100):
        matrix[i, j] = [(i % bits), (i % bits), (i % bits)]
        

color_mapped_image = cv2.applyColorMap(matrix, fastiecm)

cv2.imshow('Legend', color_mapped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 1 -> purple
# 0.1 -> blue
# green ->160 -> 0.25
# yellow -> 200 -> 0.57
# brown -> 215 -> 0.69
# red -> 240 ->0.88

# -1 -> white


# NDVI = 2*Color/255 - 1

