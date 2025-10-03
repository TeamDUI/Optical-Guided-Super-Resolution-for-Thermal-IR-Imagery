import rasterio
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import rasterio
import matplotlib.pyplot as plt

def main(filename):
    with rasterio.open(filename) as src:
        red  = src.read(4)
        green = src.read(3)
        blue  = src.read(2)

    gray = 0.2989 * red + 0.5870 * green + 0.1140 * blue
    gray_norm = (gray - gray.min()) / (gray.max() - gray.min())

    plt.figure(figsize=(8, 8))
    plt.imshow(gray_norm)
    plt.title("Lumina")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        filename = str(input("Enter the filename: "))
    else:
        filename = sys.argv[1]
    main(filename)