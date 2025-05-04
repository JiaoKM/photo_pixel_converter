import io
import json
import numpy as np
import streamlit as st
from PIL import Image
from rembg import remove

from utils import *

lang = st.sidebar.selectbox("🌐 Language / 语言", ["简体中文", "English"])
with open("config/lang.json", 'r', encoding='utf-8') as f:
    lang_dict = json.load(f)
tr = lang_dict[lang]

with open("config/palette.json", 'r', encoding='utf-8') as f:
    palettes = json.load(f)

st.title(tr['title'])

st.text(tr['introduction'])

uploaded_file = st.file_uploader(tr['upload'], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img_bytes_io = uploaded_file.getvalue()
    image = Image.open(uploaded_file).convert("RGBA")
    st.image(image, caption=tr['ori_img'], use_container_width=True)
    
    # 增加背景去除功能
    rmbg_flag = st.checkbox(tr['remove_background'], value=False)
    if rmbg_flag:
        result = remove(img_bytes_io)
        image = Image.open(io.BytesIO(result)).convert("RGBA")
        st.image(image, caption=tr['image_removed_bg'], use_container_width=True)

    image = np.array(image)

    # 选择一个像素的大小
    pixel_size = st.slider(tr["pixel_size_select"], 2, 64, 16)
    
    # 增加图片裁剪功能
    st.markdown("### " + tr['cropping'])
    left_ratio = st.slider(tr["left_crop_ratio"], 0, 100, 0)
    right_ratio = st.slider(tr["right_crop_ratio"], 0, 100, 0)
    top_ratio = st.slider(tr["top_crop_ratio"], 0, 100, 0)
    bottom_ratio = st.slider(tr["bottom_crop_ratio"], 0, 100, 0)
    image = image_crop(image, left_ratio, right_ratio, top_ratio, bottom_ratio)

    # 根据像素大小重置图片大小
    image = resize_image_pixel(image, pixel_size)

    # 选择一种调色盘
    palette_name = st.selectbox(
        tr['palette_select'],
        ['None', 'Auto(K-Means)', 'Manual'] + list(palettes.keys())
        )
    
    if palette_name == 'None':
        # 最简易像素处理
        image = pixelate(image, pixel_size)
    elif palette_name == 'Auto(K-Means)':
        # 使用K-Means自动生成一个调色板，用户可以控制颜色数量
        color_num = st.slider(tr["kmeans_color_num"], 4, 32, 10)
        palette_kmeans = generate_palette_kmeans(image, color_num)
        image = pixelate(image, pixel_size, palette_kmeans)
    elif palette_name == 'Manual':
        # 用户手动选择颜色生成一个调色盘，可上传或下载调色盘json文件
        st.markdown("### " + tr['manual_palette'])
        # 初始化调色盘中的颜色
        if 'custom_palette' not in st.session_state:
            st.session_state.custom_palette = [[0, 0, 0]]
        # 添加颜色
        new_color = st.color_picker(tr['color_select'], '#ffffff')
        if st.button(tr['add_to_palette']):
            rgb = [int(new_color.lstrip('#')[i: i + 2], 16) for i in [0, 2, 4]]
            if rgb not in st.session_state.custom_palette:
                st.session_state.custom_palette.append(rgb)
            else:
                st.warning(tr['color_exists'])

        # 显示当前调色盘
        if st.session_state.custom_palette:
            st.markdown("#### " + tr['current_palette'])
            for i, color in enumerate(st.session_state.custom_palette):
                col1, col2, col3 = st.columns([1, 4, 1])
                with col1:
                    st.markdown(f"#{i+1}")
                with col2:
                    st.color_picker(label=str(color[0]) + " " + str(color[1]) + " " + str(color[2]), 
                                    value=rgb_to_hex(color), 
                                    key=f"display_{i}", 
                                    disabled=False)
                with col3:
                    if st.button("❌", key=f"delete_{i}"):
                        st.session_state.custom_palette.pop(i)
        else:
            st.info(tr['no_colors'])

        # 上传JSON文件
        st.markdown("#### " + tr['upload_palette'])
        palette_json = st.file_uploader(tr['choose_palette_json'], type=['json'])
        if palette_json:
            try:
                st.session_state.custom_palette = json.load(palette_json)
            except Exception as e:
                st.error(f"{tr['palette_load_fail']}: {e}")

        # 下载JSON按钮
        if st.session_state.custom_palette:
            json_str = json.dumps(st.session_state.custom_palette, indent=4)
            st.download_button(
                label=tr.get("download_palette", "下载调色盘 JSON"),
                data=json_str,
                file_name="custom_palette.json",
                mime="application/json"
            )

        image = pixelate(image, pixel_size, st.session_state.custom_palette)
    else:
        image = pixelate(image, pixel_size, palettes[palette_name])

    image = Image.fromarray(image, mode="RGBA")
    st.image(image, caption=tr['pixel_art'], use_container_width=True)

    # 转成 BytesIO 流
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    file_name = 'pixel_art_' + str(pixel_size) + '_' + palette_name + '.png'

    # 下载按钮
    st.download_button(
        label=tr['download'],
        data=img_bytes,
        file_name=file_name,
        mime="image/png"
    )

