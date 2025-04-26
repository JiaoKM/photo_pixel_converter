import cv2
import json
import numpy as np
from rembg import remove
from sklearn.cluster import KMeans

def resize_image_pixel(image, pixel_size):
    # 根据像素大小重置图片大小
    height, width = image.shape[:2]
    resized_width = round(width / pixel_size) * pixel_size
    resized_height = round(height / pixel_size) * pixel_size
    return cv2.resize(image, (resized_width, resized_height))

def apply_palette(image, palette):
    # 使用调色盘更改颜色
    height, width = image.shape[:2]
    img_flat = image[:, :, :3].reshape(-1, 3)

    palette = np.array(palette)

    distances = np.linalg.norm(img_flat[:, None, :] - palette[None, :, :], axis=2)

    nearest_color_idx = np.argmin(distances, axis=1)

    mapped_flat = palette[nearest_color_idx]

    mapped_img = mapped_flat.reshape((height, width, 3)).astype(np.uint8)

    image[:, :, :3] = mapped_img

    return image

def generate_palette_kmeans(image, color_num):
    # 使用K-Means聚类根据颜色数量生成调色盘
    img_flat = image[:, :, :3].reshape(-1, 3)
    kmeans = KMeans(n_clusters=color_num, random_state=42).fit(img_flat)
    palette = kmeans.cluster_centers_.astype(int)
    return palette.tolist()

def pixelate(image, pixel_size, palette=None):
    # 简易的像素处理
    height, width = image.shape[:2]
    pixel_image = cv2.resize(image, (width // pixel_size, height // pixel_size), interpolation=cv2.INTER_LINEAR)
    if palette != None:
        pixel_image = apply_palette(pixel_image, palette)
    return pixel_image


if __name__ == "__main__":
    with open("config/palette.json", 'r', encoding='utf-8') as f:
        palettes = json.load(f)
    test_image = cv2.imread("test_image.jpg")
    image = resize_image_pixel(test_image, 16)
    image = pixelate(image, 16)
    palette_kmeans = generate_palette_kmeans(image, 10)
    image = pixelate(image, 16, palette_kmeans)
    pass