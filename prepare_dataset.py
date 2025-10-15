import sys
import numpy as np
import cv2
import rasterio
from rasterio.transform import Affine
import os


def main():
    if len(sys.argv) < 2:
        print("Usage: python prepare_dataset.py <dir>")
        sys.exit(1)

    folder_path = sys.argv[1]
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    print(folders)
    print(len(folders))

    for i in folders:
        folder = [f for f in os.listdir(f"{folder_path}/{i}") if os.path.isdir(os.path.join(f"{folder_path}/{i}", f))]
        tif_path = f"{folder_path}/{i}/{folder[0]}/all_bands.tif"

        with rasterio.open(tif_path) as src:
            blue  = src.read(2).astype(np.float32)
            green = src.read(3).astype(np.float32)
            red   = src.read(4).astype(np.float32)

            meta = src.meta.copy()

        rgb = np.dstack([red, green, blue])

        rgb_min, rgb_max = np.min(rgb), np.max(rgb)
        if rgb_max > 255:
            rgb = (255 * (rgb - rgb_min) / (rgb_max - rgb_min + 1e-8)).astype(np.uint8)
        else:
            rgb = rgb.astype(np.uint8)

        grayscale = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

        scale_factor = 100 / 30
        h, w = grayscale.shape
        new_h = int(round(h / scale_factor))
        new_w = int(round(w / scale_factor))

        meta.update({
            "count": 1,
            "height": h,
            "width": w
        })

        out_path = f"super-resolution/HR/img_{i}_hr.tif"
        with rasterio.open(out_path, "w", **meta) as dst:
            dst.write(grayscale, 1)

        grayscale_down = cv2.resize(
            grayscale,
            (new_w, new_h),
            interpolation=cv2.INTER_AREA
        )

        grayscale_restored = cv2.resize(
            grayscale_down,
            (w, h),
            interpolation=cv2.INTER_CUBIC
        )

        meta.update({
            "count": 1,
            "height": h,
            "width": w
        })

        out_path = f"super-resolution/LR/img_{i}_lr.tif"
        with rasterio.open(out_path, "w", **meta) as dst:
            dst.write(grayscale_restored, 1)

        print(f"Processed file {tif_path}")

if __name__ == "__main__":
    main()
