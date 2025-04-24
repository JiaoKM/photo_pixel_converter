import cv2
import numpy as np
import streamlit as st
from PIL import Image
from rembg import remove

def resize_image_pixel(image, pixel_size):
    # 根据像素大小重置图片大小
    height, width = image.shape[:2]
    resized_width = round(width / pixel_size) * pixel_size
    resized_height = round(height / pixel_size) * pixel_size
    return cv2.resize(image, (resized_width, resized_height))

def pixelate(image, pixel_size):
    # 简易的像素处理
    height, width = image.shape[:2]
    return cv2.resize(image, (width // pixel_size, height // pixel_size), interpolation=cv2.INTER_LINEAR)


if __name__ == "__main__":
    test_image = cv2.imread("test_image.jpg")
    image = resize_image_pixel(test_image, 16)
    pass