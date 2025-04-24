import io
import json
import streamlit as st
from PIL import Image

from utils import *

st.title("Photo pixel converter")

# 上传图片
uploaded_file = st.file_uploader("上传一张图片", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="原始图片", use_column_width=True)

    # 输入新的尺寸
    st.subheader("输入新的尺寸")
    width = st.number_input("宽度（px）", min_value=1, value=image.width)
    height = st.number_input("高度（px）", min_value=1, value=image.height)

    # 调整大小
    if st.button("调整图片大小"):
        resized_image = image.resize((width, height))
        st.image(resized_image, caption="调整后的图片", use_column_width=True)

        # 保存为 BytesIO 以供下载
        img_byte_arr = io.BytesIO()
        resized_image.save(img_byte_arr, format=image.format)
        img_byte_arr = img_byte_arr.getvalue()

        # 下载链接
        st.download_button(
            label="下载调整后的图片",
            data=img_byte_arr,
            file_name=f"resized_image.{image.format.lower()}",
            mime=f"image/{image.format.lower()}"
        )


