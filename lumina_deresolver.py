import sys
import numpy as np
import cv2
import rasterio
from rasterio.transform import Affine

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_landsat.py <all_band.tif>")
        sys.exit(1)

    tif_path = sys.argv[1]

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

    out_path = "grayscale_down_up_same_shape.tif"
    with rasterio.open(out_path, "w", **meta) as dst:
        dst.write(grayscale_restored, 1)

    print("saved")

if __name__ == "__main__":
    main()
