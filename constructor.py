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

    rgb = np.dstack((red, green, blue))
    rgb_norm = (rgb - rgb.min()) / (rgb.max() - rgb.min())

    plt.figure(figsize=(8, 8))
    plt.imshow(rgb_norm)
    plt.title("RGB Composite (Bands 4-3-2)")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        filename = str(input("Enter the filename: "))
    else:
        filename = sys.argv[1]
    main(filename)