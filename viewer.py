import sys
import math
import rasterio
import matplotlib.pyplot as plt

def main(filename):
    with rasterio.open(filename) as src:
        bands = src.count
        print(f"Number of bands: {bands}")
        print(src.res)

        cols = math.ceil(math.sqrt(bands))
        rows = math.ceil(bands / cols)

        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
        if bands == 1:
            axes = [axes]
        else:
            axes = axes.flatten()

        for i in range(bands):
            band = src.read(i + 1)
            print(band.shape)
            im = axes[i].imshow(band)
            axes[i].set_title(" ")
            axes[i].axis("off")
            cbar = plt.colorbar(im, ax=axes[i], fraction=0.046, pad=0.04)
            cbar.set_label(f"Pixel Value Band {i+1}", rotation=270, labelpad=15)

        for j in range(bands, len(axes)):
            axes[j].axis("off")

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        filename = str(input("Enter the filename: "))
    else:
        filename = sys.argv[1]

    main(filename)
